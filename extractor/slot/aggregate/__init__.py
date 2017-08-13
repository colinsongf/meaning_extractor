# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.slot.match import Match

import copy
import re

class Aggregate(object):
  """
  Aggregate slot containing basic slots and other mixed expressions. For example one might wish to create the STDateTime
  aggregate slot type if STDate and STTime are already implemented.
  """

  """
  Override.
  An identifier used for specifying the type of slot to match for in aggregate rules.
  For example, an aggregate rule matching for STDateTime with identifier st_datetime may specify:
  {timestamp:st_datetime}. All inheriting classes should override this identifier.
  """
  _slot_type_identifier = 'aggregate'

  """
  Override.
  A dictionary of {identifier : [rule]}, where rules is a list of regular expressions or strings which can be used to
  match strings. identifier may be helpful to specify how exactly the matched string should be resolved / interpreted.

  The aggregate rule supports a few things on top of the base slot types:

    * Alternatives: '[choice_a|choice_b]'
    * Optional: '(optional )content'
    * Slots: '{timestamp:st_datetime}'
    * Any one character: 'The?e is exactly one character'
    * Any string of characters: 'Any* would work'
  """
  _rules = dict()

  """
  Override.
  Inheriting classes may override this with the following types:

    * None (not overriding) - the identifier does not entail auxiliary information
    * function - the auxiliary information will be extracted by invoking
      _resolve(identifier, synonym_matching, matched_obj)
    * dict - the resolution function will use the one specified in the dictionary (by identifier),
      and auxiliary information will be similarly extracted by invoking
      cls._resolve(identifier, synonym_matching, matched_obj).
      If the resolution function for a particular synonym is not specified. No auxiliary information will be
      returned.

  The resolve function should return an interpretation of the actual matched string. If the matched string does not make
  sense, None should be returned.
  """
  _resolve = None

  # Do not override
  _validated_and_standardized = False
  _rules_standard = dict()

  # Do not touch or override below

  __REGEX_SLOT_VARIABLES = r'[_a-z]\w*'
  __REGEX_SLOT = r'\{{(?P<slot_key>{}):(?P<slot_type>{})\}}'.format(
    __REGEX_SLOT_VARIABLES, __REGEX_SLOT_VARIABLES)

  __REGEX_ALTERNATIVES = r'\[(\w*(\|\w*)*)\]'
  __REGEX_ALTERNATIVES_STD = lambda o: r'(?:{})'.format('|'.join(sorted(o.group(1).split('|'), key=len, reverse=True)))

  @classmethod
  def __collate_capture_groups(cls, raw_rule):
    expr = ''.join(c for c in raw_rule if c != ' ')

    # Record the slots in this expression. If there are multiple consecutive slots, merge them into a single capture
    # group, however recording the corresponding slots.

    # For example, in the case of '{slot_1, slot_type1}{slot_2, slot_type2}', we wish to merge them into a single
    # capture group: '(?P<s1>\w+)'. However, we still record the slots corresponding to capture group s1.
    slot_keys = set()
    capture_group_slot_mapping = dict()
    previous_slot_end = None

    def repl(var):
      nonlocal previous_slot_end
      new_capture_group = False
      if var.span(0)[0] != previous_slot_end:
        new_capture_group = True
        capture_group_slot_mapping['s{}'.format(len(capture_group_slot_mapping))] = []

      capture_group_name = 's{}'.format(len(capture_group_slot_mapping) - 1)
      slot_key = var.groupdict()['slot_key']
      capture_group_slot_mapping[capture_group_name].append(
        (slot_key, var.groupdict()['slot_type']))

      if slot_key in slot_keys:
        raise Exception('Multiple slots with name: {}'.format(slot_key))
      slot_keys.add(slot_key)

      previous_slot_end = var.span(0)[1]
      regex_replace = r'(?P<{}>\w+)' # \
        # if (previous_slot_end == len(expr) or not expr[previous_slot_end].isalnum()) else r'(?P<{}>\w+?)'

      return regex_replace.format(capture_group_name) if new_capture_group else r''

    expr = re.sub(cls.__REGEX_SLOT, repl, expr)
    expr = r'{}'.format(expr)
    return (expr, capture_group_slot_mapping)

  @classmethod
  def __expand_rules_recrusive(cls, rule, cursor, lparen_cnt, so_far, all_rules):
    least_lparen_cnt = lparen_cnt

    while cursor < len(rule):
      if rule[cursor] not in '()':
        if lparen_cnt <= least_lparen_cnt:
          so_far.append(rule[cursor])
      elif rule[cursor] == '(':
        if lparen_cnt <= least_lparen_cnt:
          cls.__expand_rules_recrusive(rule, cursor + 1, lparen_cnt + 1, so_far[:], all_rules)
        lparen_cnt += 1
      else:
        # == ')'
        lparen_cnt -= 1
        least_lparen_cnt = min(lparen_cnt, least_lparen_cnt)
        if lparen_cnt < 0:
          raise Exception('Invalid rule: {}'.format(rule))
      cursor += 1

    if lparen_cnt != 0:
      raise Exception('Invalid rule: {}'.format(rule))

    all_rules.append(''.join(so_far))
    return all_rules

  @classmethod
  def __apply_transform(cls, rule):
    rule = re.sub(cls.__REGEX_ALTERNATIVES, cls.__REGEX_ALTERNATIVES_STD, rule)
    return rule

  @classmethod
  def __standardize_and_expand_rule(cls, rule, seen_rules):
    """
    Parse the sample utterance provided by user. Dynamically convert the expression into a regex that can be used to
    match against a sample utterance. Returns the regex and also a dictionary which records the mappings from capture
    group name to slot names.

    Raise exception if the provided utterance is invalid or contains ambiguous expressions.
    """
    all_expanded_rules = []
    so_far, all_rules = [], []
    cls.__expand_rules_recrusive(rule, 0, 0, so_far, all_rules)
    filtered_rules = []
    for expanded_rule in all_rules:
      expanded_rule = cls.__apply_transform(expanded_rule)
      if expanded_rule in seen_rules:
        # print('Warning: Two different specified matching \'{}\' and \'{}\' yield a same rule: {}. Ignoring...'.format(
          # seen_rules[expanded_rule], rule, expanded_rule))
        pass
      else:
        seen_rules[expanded_rule] = rule
        filtered_rules.append(expanded_rule)
    return [cls.__collate_capture_groups(rule) for rule in filtered_rules if rule]

  @classmethod
  def __validate_and_standardize(cls):
    if cls._validated_and_standardized:
      return
    cls._rules_standard = dict()

    # Validate _rules
    if not isinstance(cls._rules, dict):
      raise Exception('_rules must be a dict.')
    for identifier, rules in cls._rules.items():
      if not isinstance(identifier, str):
        raise Exception('Each identifier must be a string.')
      if not isinstance(rules, list):
        raise Exception('The rules must be a list.')
      for rule in rules:
        if not (isinstance(rule, str) or isinstance(rule, cls.__compiled_re_type)):
          raise Exception('Each rule must be a string or a compiled regex.')

    # Validate _resolve
    if not (cls._resolve is None or isinstance(cls._resolve, dict) or callable(cls._resolve)):
      raise Exception('_resolve must be None, a function or a dictionary.')
    if isinstance(cls._resolve, dict):
      for identifier, func in cls._resolve.items():
        if not callable(func):
          raise Exception('Each _resolve dictionary value should be a function.')

    # Standardize rules
    seen_rules = dict()
    for identifier, rules in cls._rules.items():
      cls._rules_standard[identifier] = [(rule, cls.__standardize_and_expand_rule(rule, seen_rules)) for rule in rules]

    cls._validated_and_standardized = True

  @classmethod
  def __consume_recursive(cls, query, start, end, slots, slots_i, aggregate_path, solutions):
    if slots_i == len(slots) and start == end:
      solutions.append(copy.deepcopy(aggregate_path))
      return

    if slots_i == len(slots) or start == end:
      return

    (slot_key, slot_type) = slots[slots_i]
    from extractor.slot.all import Slot
    slot_class = Slot.with_identifier(slot_type)
    matches = slot_class.consume(query, start, end)
    if not matches:
      return
    for match in matches:
      aggregate_path.append(match)
      cls.__consume_recursive(query, match.end, end, slots, slots_i + 1, aggregate_path, solutions)
      aggregate_path.pop()

  @classmethod
  def consume(cls, query, start=0, end=None, greedy=False):
    """
    Attempt to consume from the specified start not exceeding the specified end, a substring that matches this slot
    type. Returns a list of Match objects.
    """
    cls.__validate_and_standardize()

    all_matches = []
    if end is None:
      end = len(query)

    for identifier, rules in cls._rules_standard.items():
      for rule_i, (raw_rule, expanded_rules) in enumerate(rules):
        for (rule, capture_group_slot_mapping) in expanded_rules:
          regex_rule = re.compile(rule) if isinstance(rule, str) else rule
          match_obj = regex_rule.match(query, start, end)
          if match_obj is not None:
            slot_match_end = match_obj.span(0)[1]
            slot_key_value_mappings = dict()
            num_sub_slots_to_be_matched = 0
            for i, (capture_group_name, slots) in enumerate(sorted(list(capture_group_slot_mapping.items()))):
              # 0, ('s0', [('timestamp', 'type_datetime'), ('num_people', 'type_people')])
              aggregate_path, solutions = [], []
              num_sub_slots_to_be_matched += len(slots)
              cls.__consume_recursive(query, match_obj.span(capture_group_name)[0],
                match_obj.span(capture_group_name)[1], slots, 0, aggregate_path, solutions)
              for solution in solutions:
                if match_obj.span(0)[1] == match_obj.span(capture_group_name)[1]:
                  slot_match_end = solution[-1].end
                slot_value = query[start:slot_match_end]
                assert len(solution) == len(slots)
                for (slot_i, (slot_key, slot_type)) in enumerate(slots):
                  solution[slot_i].set_slot_key(slot_key)
                  slot_key_value_mappings[slot_key] = solution[slot_i]

            if len(slot_key_value_mappings) != num_sub_slots_to_be_matched:
              continue
            if callable(cls._resolve):
              slot_value = cls._resolve(identifier, cls._rules[identifier][rule_i],
                match_obj, slot_key_value_mappings)
            elif identifier in cls._resolve:
              slot_value = cls._resolve[identifier](identifier, cls._rules[identifier][rule_i],
                match_obj, slot_key_value_mappings)
            if slot_value is not None:
              all_matches.append(Match(query, start, slot_match_end, cls, slot_value,
                cls._rules[identifier][rule_i], rule, capture_group_slot_mapping))

    if not greedy or not all_matches:
      return all_matches
    return [max(all_matches, key=lambda m: m.end - m.start)]
