# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.slot.all import Slot

import copy
import re

class Aggregate(Base):
  """
  Aggregate slot containing basic slots and other mixed expressions. Can be used for sample utterances.
  Converts sample utterance format into standardized regex format. Slots will be converted into wild case. The
  validation of the slots should be handled later by the invoker of the parser.
  """

  _identifier = 'aggregate'

  _rules_standard = dict()
  _rules_have_been_standardized = False

  # No validation / resolution for aggregate slot types
  _validation = None
  _validation_validated = None

  __REGEX_ALTERNATIVES = r'\[(\w+(\|\w+)*)\]'
  __REGEX_ALTERNATIVES_STD = r'(?:\1)'

  __REGEX_OPTIONAL = r'\((\w+)\)'
  __REGEX_OPTIONAL_STD = r'(?:\1)?'

  __REGEX_LITERAL = r'(\w+)'
  __REGEX_LITERAL_STD = r'\1'

  __REGEX_QUESTION = r'\?'
  __REGEX_QUESTION_STD = r'\w*'

  __REGEX_STAR = r'\*'
  __REGEX_STAR_STD = r'\w+'

  __REGEX_SLOT_VARIABLES = r'[_a-z]\w*'
  __REGEX_SLOT = r'\{{(?P<slot_name>{}):(?P<slot_type>{})\}}'.format(__REGEX_SLOT_VARIABLES, __REGEX_SLOT_VARIABLES)

  REGEX_VALID_EXPRESSION = r'(({})*({})*({})*({})*({})*)+'.format(
    __REGEX_ALTERNATIVES, __REGEX_OPTIONAL, __REGEX_SLOT, __REGEX_LITERAL, __REGEX_STAR)

  @classmethod
  def _standardize_expression(cls, expr_raw):
    """
    Parse the sample utterance provided by user. Dynamically convert the expression into a regex that can be used to
    match against a sample utterance. Returns the regex and also a dictionary which records the mappings from capture
    group name to slot names.

    Raise exception if the provided utterance is invalid or contains ambiguous expressions.
    """

    expr = ''.join(c for c in expr_raw if c != ' ')
    if re.match(cls.REGEX_VALID_EXPRESSION, expr) is None:
      raise Exception('Utterance expression format invalid.')

    # Standardize expression into the regex format.
    expr = re.sub(cls.__REGEX_STAR, cls.__REGEX_STAR_STD, expr)
    expr = re.sub(cls.__REGEX_QUESTION, cls.__REGEX_QUESTION_STD, expr)
    expr = re.sub(cls.__REGEX_LITERAL, cls.__REGEX_LITERAL_STD, expr)
    expr = re.sub(cls.__REGEX_ALTERNATIVES, cls.__REGEX_ALTERNATIVES_STD, expr)
    expr = re.sub(cls.__REGEX_OPTIONAL, cls.__REGEX_OPTIONAL_STD, expr)

    # If there are multiple consecutive wild cards, the expression is invalid.
    if re.search(r'\\w\+\\w\+', expr):
      raise Exception('Multiple consecutive wild cards.')

    # Record the slots in this expression. If there are multiple consecutive slots, merge them into a single capture
    # group, however recording the corresponding slots.

    # For example, in the case of '{slot_1, slot_type1}{slot_2, slot_type2}', we wish to merge them into a single
    # capture group: '(?P<s1>\w+)'. However, we still record the slots corresponding to capture group s1.
    slot_names = set()
    capture_group_slot_matchings = dict()
    previous_slot_end = None

    def repl(var):
      nonlocal previous_slot_end
      new_capture_group = False
      if var.span(0)[0] != previous_slot_end:
        new_capture_group = True
        capture_group_slot_matchings['s{}'.format(len(capture_group_slot_matchings))] = []

      capture_group_name = 's{}'.format(len(capture_group_slot_matchings) - 1)
      slot_name = var.groupdict()['slot_name']
      capture_group_slot_matchings[capture_group_name].append(
        (slot_name, var.groupdict()['slot_type']))

      if slot_name in slot_names:
        raise Exception('Multiple slots with name: {}'.format(slot_name))
      slot_names.add(slot_name)

      previous_slot_end = var.span(0)[1]
      return r'(?P<{}>\w+)'.format(capture_group_name) if new_capture_group else r''

    expr = re.sub(cls.__REGEX_SLOT, repl, expr)
    expr = r'{}'.format(expr)

    return (expr, capture_group_slot_matchings)

  @classmethod
  def _standardize_rules(cls):
    if cls._rules_have_been_standardized:
      return
    for identifier, synonym_matchings in cls._rules.items():
      cls._rules_standard[identifier] = [cls._standardize_expression(synonym) for synonym in synonym_matchings]

    cls._rules_have_been_standardized = True

  @classmethod
  def _validate_validation(cls):
    raise Exception('Validation should not be invoked for aggregate slot types.')

  @classmethod
  def _consume_recursive(cls, query, start, end, slots, slots_i, aggregate_path, solutions):
    if start == end:
      if slots_i == len(slots):
        solutions.append(copy.deepcopy(aggregate_path))
      return

    (slot_name, slot_type) = slots[slots_i]
    slot_class = Slot.with_identifier(slot_type)
    matches = slot_class.consume(query, start, end)
    if not matches:
      return
    if isinstance(slot_class, Base):
      for (identifier, synonym_matching, synonym_match_obj) in matches:
        aggregate_path.append((identifier, synonym_matching, synonym_match_obj))
        cls._consume_recursive(query, synonym_match_obj.span(0)[1], end, slots, slots_i + 1, aggregate_path)
        aggregate_path.pop()
    elif isinstance(slot_class, Aggregate):
      for (identifier, synonym_matching, resolution) in matches:
        aggregate_path.append((identifier, synonym_matching, resolution))
        cls._consume_recursive(query, synonym_match_obj.span(0)[1], end, slots, slots_i + 1, aggregate_path)
        aggregate_path.pop()
    else:
      raise Exception('Slot must either be an instance of Base or Aggregate.')

    slots_i += 1

  @classmethod
  def consume(cls, query, start=0, end=None):
    cls._validate_rules()
    cls._standardize_rules()

    if end is None:
      end = len(query)

    # Attempt to consume an identifier from query start. For each successful consumption, record the
    # (identifier, synonym_matching, matched_obj) tuple.
    for identifier, (synonym_rules, capture_group_slot_matchings) in cls._rules_standard.items():
      for synonym_matching in synonym_rules:
        if isinstance(synonym_matching, str):
          synonym_matching = re.compile(synonym_matching, re.UNICODE)
        synonym_match_obj = synonym_matching.match(query, start, end)
        if synonym_match_obj is not None:
          # Attempt to recover all matchings that could be possible.
          for capture_group_slot_name, slots in capture_group_slot_matchings.items():
            # s0, [('timestamp', 'type_datetime'), ('num_people', 'type_people')]
            pass
