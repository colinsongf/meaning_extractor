# -*- coding: utf-8 -*-

from extractor.match import MatchAny, MatchSlot, MatchLiteral, MatchUtterance
from extractor.utility.rule import Rule

import copy

class Utterance(object):
  """
  Utterance classes are used for defining and matching sentences according to preset rules.
  """

  """
  All inheriting classes should override this identifier
  """
  _utterance_identifier = 'utterance'


  """
  Override.
  A dictionary of {identifier : [rule]}, where [rule] is a list of regular expressions or strings which can be used to
  match strings. Identifier may be helpful to specify how exactly the matched string should be resolved / interpreted.

  The utterance rule supports the following rule components:

    * Literal: 'abc'
    * Alternatives: '[choice_a|choice_b]'
    * Optional: '(optional )content'
    * Slots: '{timestamp:st_datetime}'
    * Any string of characters: 'Any* would work'

  A sample utterance rule may look like:

    'Reserve a meeting room (of {num_people:st_number}) at {time:st_datetime}*'
  """
  _rules = dict()

  # Do not override
  _validated_and_standardized = False
  _rules_standard = dict()

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
        if not isinstance(rule, str):
          raise Exception('Each rule must be a string or a compiled regex.')

    # Standardize rules
    seen_rules = dict()
    for identifier, rules in cls._rules.items():
      cls._rules_standard[identifier] = [(rule, Rule.standardize_and_expand(rule, seen_rules, True)) for rule in rules]

    cls._validated_and_standardized = True

  @classmethod
  def __consume_recursive(cls, query, start, match_segments, match_segments_i, aggregate_matches, solutions):
    if match_segments_i == len(match_segments):
      solutions.append(copy.copy(aggregate_matches))
      return True
    match_segment = match_segments[match_segments_i]
    all_matches = match_segment.consume_query(query, start)
    any_path = False
    for match in all_matches:
      aggregate_matches.append(match)
      any_path = (cls.__consume_recursive(
        query, match.match_end, match_segments, match_segments_i + 1, aggregate_matches, solutions)) or any_path
      aggregate_matches.pop()

    return any_path

  @classmethod
  def match(cls, query, exact_match=False):
    cls.__validate_and_standardize()

    all_matches = []

    for identifier, rules in cls._rules_standard.items():
      for rule_i, (raw_rule, expanded_rules) in enumerate(rules):
        for (rule, match_segments) in expanded_rules:
          if not match_segments:
            continue
          search_start_end = 1 if exact_match else len(query)
          for start in range(0, search_start_end):
            aggregate_matches, solutions = [], []
            any_path = cls.__consume_recursive(query, start, match_segments, 0, aggregate_matches, solutions)
            if not any_path:
              continue
            for solution in solutions:
              slot_key_value_mappings = dict()
              if not solution:
                continue
              for match in solution:
                if isinstance(match, MatchSlot):
                  slot_key_value_mappings[match.slot_key] = match
              all_matches.append(MatchUtterance(query, start, solution[-1].match_end, identifier,
                cls._rules[identifier][rule_i], rule, slot_key_value_mappings, solution))

    if not all_matches:
      return all_matches

    # Max slots
    max_slot_match_obj = max(all_matches, key=lambda m: len(m.slot_mappings))
    max_slot_match = len(max_slot_match_obj.slot_mappings)
    max_slot_matches = [m for m in all_matches if len(m.slot_mappings) == max_slot_match]

    # Max length
    max_len_match = max(max_slot_matches, key=lambda m: m.match_end - m.match_start)
    max_len = max_len_match.match_end - max_len_match.match_start
    max_len_matches = [m for m in max_slot_matches if m.match_end - m.match_start == max_len]

    # Max literal match length
    literal_len_func = lambda m: sum(seg.match_end - seg.match_start \
      for seg in m.match_segments if isinstance(seg, MatchLiteral))
    max_literal_match = max(max_len_matches, key=literal_len_func)
    max_literal_match_len = literal_len_func(max_literal_match)
    max_literal_matches = [m for m in max_len_matches if literal_len_func(m) == max_literal_match_len]

    # Min literal any match length
    any_literal_len_func = lambda m: sum(seg.match_end - seg.match_start \
      for seg in m.match_segments if isinstance(seg, MatchAny))
    min_any_literal_match = min(max_literal_matches, key=any_literal_len_func)
    min_any_literal_match_len = any_literal_len_func(min_any_literal_match)
    min_any_literal_matches = [m for m in max_literal_matches if any_literal_len_func(m) == min_any_literal_match_len]

    return min_any_literal_matches
