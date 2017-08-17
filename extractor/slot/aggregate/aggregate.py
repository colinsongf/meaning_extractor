# -*- coding: utf-8 -*-

from extractor.match import MatchSlot
from extractor.slot.base import Base
from extractor.utility.rule import Rule

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
  For example, an aggregate rule matching for STDateTime with identifier 'st_datetime' may specify:
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
  """
  _rules = dict()

  """
  Override.
  Inheriting classes may override this with the following types:

    * None (not overriding) - the identifier does not entail auxiliary information
    * function - the auxiliary information will be extracted by invoking
      _resolve_aggregate(identifier, raw_rule, expanded_rule, match_end, consumed_query, slot_key_value_mappings)
    * dict - the resolution function will use the one specified in the dictionary (by identifier),
      and auxiliary information will be similarly extracted by invoking
      cls._resolve_aggregate(identifier, raw_rule, expanded_rule, match_end, consumed_query, slot_key_value_mappings).
      If the resolution function for a particular synonym is not specified. No auxiliary information will be
      returned.

  The resolve function should return an interpretation of the actual matched string. If the matched string does not make
  sense, None should be returned.
  """
  _resolve_aggregate = lambda identifier, raw_rule, expanded_rule, match_end, consumed_query, slot_key_value_mappings: \
    consumed_query

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
          raise Exception('Each rule must be a string.')

    # Validate _resolve_aggregate
    if not (cls._resolve_aggregate is None or isinstance(cls._resolve_aggregate, dict) or callable(cls._resolve_aggregate)):
      raise Exception('_resolve_aggregate must be None, a function or a dictionary.')
    if isinstance(cls._resolve_aggregate, dict):
      for identifier, func in cls._resolve_aggregate.items():
        if not callable(func):
          raise Exception('Each _resolve_aggregate dictionary value should be a function.')

    # Standardize rules
    seen_rules = dict()
    for identifier, rules in cls._rules.items():
      cls._rules_standard[identifier] = [(rule, Rule.standardize_and_expand(rule, seen_rules, False)) for rule in rules]

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
  def consume(cls, query, start, greedy=False):
    """
    Attempt to consume from the specified start, a substring that matches this slot type. Returns a list of Match
    objects.
    """
    cls.__validate_and_standardize()

    all_matches = []

    # loop through each (identifier, rules) that user defined
    for identifier, rules in cls._rules_standard.items():
      for rule_i, (raw_rule, expanded_rules) in enumerate(rules):
        # loop through each expanded_rule due to usage of optionals "(...)"
        for (rule, match_segments) in expanded_rules:
          aggregate_matches, solutions = [], []
          any_path = cls.__consume_recursive(query, start, match_segments, 0, aggregate_matches, solutions)
          if not any_path:
            continue
          for solution in solutions:
            slot_key_value_mappings = dict()
            for match in solution:
              if isinstance(match, MatchSlot):
                slot_key_value_mappings[match.slot_key] = match

            match_end = solution[-1].match_end
            if callable(cls._resolve_aggregate):
              slot_value = cls._resolve_aggregate(identifier, cls._rules[identifier][rule_i], rule,
                match_end, query[:match_end], slot_key_value_mappings)
            elif identifier in cls._resolve_aggregate:
              slot_value = cls._resolve_aggregate[identifier](identifier, cls._rules[identifier][rule_i], rule,
                match_end, query[:match_end], slot_key_value_mappings)
            if slot_value is not None:
              all_matches.append(MatchSlot(
                query, start, match_end, cls, slot_value, cls._rules[identifier][rule_i], rule,
                slot_key_value_mappings, solution))

    if not all_matches or not greedy:
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
