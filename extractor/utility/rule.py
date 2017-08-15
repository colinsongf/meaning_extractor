# -*- coding: utf-8 -*-

from extractor.match_segments import MatchSegment, MatchSegmentSlot

class Rule(object):

  @classmethod
  def __extract_match_segments(cls, rule, is_utterance):
    cursor = 0
    match_segments = []
    slot_keys = set()
    while cursor < len(rule):
      (new_segment, cursor) = MatchSegment.consume_rule(rule, cursor, is_utterance)
      match_segments.append(new_segment)
      if isinstance(new_segment, MatchSegmentSlot):
        if new_segment.slot_key in slot_keys:
          raise Exception('Multiple slots with key: {}'.format(new_segment.slot_key))
        slot_keys.add(new_segment.slot_key)
    return (rule, match_segments)

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
  def standardize_and_expand(cls, rule, seen_rules, is_utterance):
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
      if expanded_rule in seen_rules:
        # print('Warning: Two different specified matching \'{}\' and \'{}\' yield a same rule: {}. Ignoring...'.format(
          # seen_rules[expanded_rule], rule, expanded_rule))
        pass
      else:
        seen_rules[expanded_rule] = rule
        filtered_rules.append(expanded_rule)
    return [cls.__extract_match_segments(rule, is_utterance) for rule in filtered_rules if rule]
