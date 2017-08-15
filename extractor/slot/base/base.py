# -*- coding: utf-8 -*-

from extractor.match import MatchSlot

import re

class Base(object):

  """
  Override.
  An identifier used for specifying the type of slot to match for in aggregate rules.
  For example, an aggregate rule matching for STDateTime with identifier st_datetime may specify:
  {timestamp:st_datetime}. All inheriting classes should override this identifier.
  """
  _slot_type_identifier = 'base'

  """
  Override.
  A dictionary of {identifier : [rule]}, where rules is a list of regular expressions or strings which can be used to
  match strings. identifier may be helpful to specify how exactly the matched string should be resolved / interpreted.
  As an example, a class to match date may specify rules as:

  _rules = {
    'day_of_week' : [r'(?:mon|tues|wednes|thurs|fri|satur|sun)day'],
    'day_of_month' : ...
  }

  Another way to use this is to think of "identifier" as a unique value, and the rules as synonyms that should all match
  to the value, for example, something like:

  _rules = {
    'cmu' : [r'cmu', r'carnegie mellon(?: university)?'],
    'stanford' : ...
  }
  """
  _rules = dict()

  """
  Override.
  Inheriting classes may override this with the following types:

    * None (not overriding) - the identifier does not entail auxiliary information
    * function - the auxiliary information will be extracted by invoking _resolve_base(identifier, rule, match_obj).
    * dict - the resolution function will use the one specified in the dictionary (by identifier),
      and auxiliary information will be similarly extracted by invoking cls._resolve_base(identifier, rule, match_obj).
      If the resolution function for a particular synonym is not specified, no auxiliary information will be returned.

  The resolve function should return an interpretation of the actual matched string. If the matched string does not make
  sense, None should be returned.
  """
  _resolve_base = lambda identifier, rule, match_obj: match_obj.group(0)

  # Do not override
  _validated = False

  @classmethod
  def _validate(cls):
    if cls._validated:
      return

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
          raise Exception('Each rule must be a string')

    # Validate _resolve_base
    if not (cls._resolve_base is None or isinstance(cls._resolve_base, dict) or callable(cls._resolve_base)):
      raise Exception('_resolve_base must be None, a function or a dictionary.')
    if isinstance(cls._resolve_base, dict):
      for rule, func in cls._resolve_base.items():
        if not callable(func):
          raise Exception('Each _resolve_base dictionary value should be a function.')

    cls._validated = True

  @classmethod
  def consume(cls, query, start, greedy=False):
    """
    Attempt to consume from the specified start, a substring that matches this slot type. Returns a list of Match
    objects.
    """
    cls._validate()
    all_matches = []

    for identifier, rules in cls._rules.items():
      for rule in rules:
        regex_rule = re.compile(rule)
        match_obj = regex_rule.match(query, start)
        if match_obj is None:
          continue

        slot_value = match_obj.group(0)
        if callable(cls._resolve_base):
          slot_value = cls._resolve_base(identifier, rule, match_obj)
        elif identifier in cls._resolve_base:
          slot_value = cls._resolve_base[identifier](identifier, rule, match_obj)
        if slot_value is not None:
          all_matches.append(MatchSlot(
            query, match_obj.span(0)[0], match_obj.span(0)[1], cls, slot_value, rule, rule, dict(), []))

    if not all_matches:
      return all_matches
    max_len_match = max(all_matches, key=lambda m: m.match_end - m.match_start)
    max_len = max_len_match.match_end - max_len_match.match_start
    return [m for m in all_matches if m.match_end - m.match_start == max_len]
