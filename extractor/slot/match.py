# -*- coding: utf-8 -*-

class Match(object):
  def __init__(self, query, start, end, slot_type, slot_value, raw_rule, matched_rule, capture_group_slot_mapping):
    assert isinstance(query, str)
    assert isinstance(start, int) and isinstance(end, int) and start <= end
    self.query = query
    self.start = start
    self.end = end
    self.slot_type = slot_type
    self.slot_value = slot_value
    self.slot_key = None
    self.raw_rule = raw_rule
    self.matched_rule = matched_rule
    self.capture_group_slot_mapping = capture_group_slot_mapping

  def set_slot_key(self, slot_key):
    self.slot_key = slot_key

  def __str__(self):
    return '[{} Match: <slot_key={}> ({}, {}) {} : {}]'.format(
      self.slot_type.__name__, self.slot_key, self.start, self.end, self.query[self.start:self.end], self.slot_value)

  def __repr__(self):
    return '[{} Match: <slot_key={}> ({}, {}) {} : {};\n raw rule: {}\n matched from regex \'{}\' with mapping {}]'.format(
      self.slot_type.__name__, self.slot_key, self.start, self.end, self.query[self.start:self.end], self.slot_value,
      self.raw_rule, self.matched_rule, self.capture_group_slot_mapping)
