# -*- coding: utf-8 -*-

class MatchSlot(object):
  def __init__(self, query, match_start, match_end, slot_type, slot_value, raw_rule, matched_rule, slot_mappings, match_segments):
    assert isinstance(query, str)
    assert isinstance(match_start, int) and isinstance(match_end, int) and match_start <= match_end
    self.query = query
    self.match_start = match_start
    self.match_end = match_end
    self.slot_type = slot_type
    self.slot_value = slot_value
    self.slot_key = None
    self.raw_rule = raw_rule
    self.matched_rule = matched_rule
    self.slot_mappings = slot_mappings
    self.match_segments = match_segments

  def set_slot_key(self, slot_key):
    self.slot_key = slot_key

  def __repr__(self):
    return '[MatchSlot ({}): <slot_key={}> ({}, {}) "{}" : {}]'.format(
      self.slot_type.__name__, self.slot_key, self.match_start, self.match_end,
        self.query[self.match_start:self.match_end], self.slot_value)

class MatchLiteral(object):
  def __init__(self, query, match_start, match_end, slot_value, raw_rule):
    assert isinstance(query, str)
    assert isinstance(match_start, int) and isinstance(match_end, int) and match_start <= match_end
    self.query = query
    self.match_start = match_start
    self.match_end = match_end
    self.slot_value = slot_value
    self.raw_rule = raw_rule

  def __repr__(self):
    return '[MatchLiteral: ({}, {}) "{}"]'.format(
      self.match_start, self.match_end,
        self.query[self.match_start:self.match_end])

class MatchAny(object):
  def __init__(self, query, match_start, match_end, slot_value):
    assert isinstance(query, str)
    assert isinstance(match_start, int) and isinstance(match_end, int) and match_start <= match_end
    self.query = query
    self.match_start = match_start
    self.match_end = match_end
    self.slot_value = slot_value

  def __repr__(self):
    return '[MatchAny: ({}, {}) "{}"]'.format(
      self.match_start, self.match_end,
        self.query[self.match_start:self.match_end])

class MatchUtterance(object):
  def __init__(self, query, match_start, match_end, rule_identifier, raw_rule, matched_rule, slot_mappings, match_segments):
    assert isinstance(query, str)
    assert isinstance(rule_identifier, str)
    if not match_start <= match_end:
      print(match_start, match_end, match_segments)
    assert isinstance(match_start, int) and isinstance(match_end, int) and match_start <= match_end
    self.query = query
    self.match_start = match_start
    self.match_end = match_end
    self.rule_identifier = rule_identifier
    self.raw_rule = raw_rule
    self.matched_rule = matched_rule
    self.slot_mappings = slot_mappings
    self.match_segments = match_segments

  def __repr__(self):
    return '[MatchUtterance: ({}, {}) "{}" with slots: {}]'.format(
      self.match_start, self.match_end,
        self.query[self.match_start:self.match_end], self.slot_mappings)
