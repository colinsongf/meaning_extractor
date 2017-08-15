# -*- coding: utf-8 -*-

from extractor.match import MatchAny, MatchSlot, MatchLiteral

import re

class STAny(object):
  pass

class MatchSegment(object):
  def __init__(self):
    raise Exception('MatchSegment object should not be initialized directly.')

  @classmethod
  def consume_rule(cls, raw_rule, start, is_utterance):
    segment_class = cls
    if raw_rule[start] == '{':
      segment_class = MatchSegmentSlot
    elif raw_rule[start] == '[':
      segment_class = MatchSegmentAlternative
    elif raw_rule[start].isalnum():
      segment_class = MatchSegmentLiteral
    else:
      if is_utterance:
        if raw_rule[start] == '*':
          segment_class = MatchSegmentAny
    if segment_class is cls:
      raise Exception('Invalid rule: {}'.format(raw_rule))
    return segment_class.consume_rule(raw_rule, start)

  def consume_query(self, query, start):
    raise Exception('Subclass must override this method.')

class MatchSegmentLiteral(MatchSegment):
  __REGEX_LITERAL = re.compile(r'\w+')

  def __init__(self, literal):
    self.literal = literal

  @classmethod
  def consume_rule(cls, raw_rule, start):
    match_obj = cls.__REGEX_LITERAL.match(raw_rule, start)
    assert match_obj is not None
    (_, end) = match_obj.span(0)
    return (cls(raw_rule[start:end]), end)

  def consume_query(self, query, start):
    all_matches = []
    if query[start:].startswith(self.literal):
      all_matches.append(MatchLiteral(query, start, start + len(self.literal), self.literal, self.literal))
    return all_matches

  def __repr__(self):
    return '<MatchSegmentLiteral \'{}\'>'.format(self.literal)

class MatchSegmentAlternative(MatchSegment):
  def __init__(self, alternatives, raw_rule):
    self.alternatives = alternatives
    self.raw_rule = raw_rule

  @classmethod
  def consume_rule(cls, raw_rule, start):
    assert raw_rule[start] == '['
    closing_brace_index = raw_rule.find(']', start + 1)
    if closing_brace_index == -1:
      raise Exception('Invalid rule: matching closing brace ] not found for rule {}'.format(raw_rule))
    raw_alternative_str = raw_rule[start + 1:closing_brace_index]
    l = raw_alternative_str.split('|')
    return (cls([s.strip() for s in l], raw_rule), closing_brace_index + 1)

  def consume_query(self, query, start):
    all_matches = []
    for alternative in self.alternatives:
      if query[start:].startswith(alternative):
        all_matches.append(MatchLiteral(query, start, start + len(alternative), alternative, self.raw_rule))
    return all_matches

  def __repr__(self):
    return '<MatchSegmentAlternative [{}]>'.format('|'.join(self.alternatives))

class MatchSegmentSlot(MatchSegment):
  def __init__(self, slot_key, slot_type):
    self.slot_key = slot_key
    self.slot_type = slot_type

  @classmethod
  def consume_rule(cls, raw_rule, start):
    assert raw_rule[start] == '{'
    closing_brace_index = raw_rule.find('}', start + 1)
    if closing_brace_index == -1:
      raise Exception('Invalid rule: matching closing brace } not found for rule: {}'.format(raw_rule))
    raw_slot_str = raw_rule[start + 1:closing_brace_index]
    l = raw_slot_str.split(':')
    if len(l) != 2:
      raise Exception('Invalid rule: slot key and / or type not specified for rule: {}'.format(raw_rule))
    slot_key, slot_type = l[0], l[1]
    return (cls(slot_key.strip(), slot_type.strip()), closing_brace_index + 1)

  def consume_query(self, query, start):
    from extractor.slot.all import Slot
    all_matches = []
    if self.slot_type != 'st_any':
      slot_class = Slot.with_identifier(self.slot_type)
      all_matches = slot_class.consume(query, start, greedy=False)
    else:
      for end in range(start, len(query) + 1):
        all_matches.append(MatchSlot(query, start, end, STAny, query[start:end], '*', '*', dict(), []))
    for match in all_matches:
      match.set_slot_key(self.slot_key)
    return all_matches

  def __repr__(self):
    return '<MatchSegmentSlot {{{}}}:{{{}}}>'.format(self.slot_key, self.slot_type)

class MatchSegmentAny(MatchSegment):
  def __init__(self):
    pass

  @classmethod
  def consume_rule(cls, raw_rule, start):
    assert raw_rule[start] == '*'
    return (cls(), start + 1)

  def consume_query(self, query, start):
    all_matches = []
    for end in range(start, len(query) + 1):
      all_matches.append(MatchAny(query, start, end, query[start:end]))
    return all_matches
