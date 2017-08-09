# -*- coding: utf-8 -*-

import re

_compiled_re_type = re.compile('').__class__

class Base(object):

  _identifier = 'base'

  # A dictionary of {identifier : synonym_rules}, where synonym_rules is a list of regular expressions
  # or strings which can be used to match strings.
  _rules = dict()
  _rules_validated = False

  # Inheriting classes may override this to validate if a given matching should be indeed an instance of this slot.
  _validation = None
  _validation_validated = False

  # Inheriting classes may override this with the following types:
  #
  #   * None (not overriding) - the identifier does not entail auxiliary information
  #   * function - the auxiliary information will be extracted by invoking
  #       _resolution(identifier, synonym_matching, matched_obj)
  #   * dict - the resolution function will use the one specified in the dictionary (by synonym_matching),
  #       and auxiliary information will be similarly extracted by invoking
  #       cls._resolution(identifier, synonym_matching, matched_obj).
  #       If the resolution function for a particular synonym is not specified. No auxiliary information will be
  #       returned.
  _resolution = None
  _resolution_validated = False

  @classmethod
  def _validate_rules(cls):
    if cls._rules_validated:
      return
    if not isinstance(cls._rules, dict):
      raise Exception('_rules must be a dict.')
    for identifier, synonyms in cls._rules.items():
      if not isinstance(identifier, str):
        raise Exception('The identifier must be a string.')
      if not isinstance(synonyms, list):
        raise Exception('The synonyms must be a list containing the synonym matchings.')
      for s in synonyms:
        if not (isinstance(s, str) or isinstance(s, _compiled_re_type)):
          raise Exception('Each entry in the synonym matching list must be a string or a compiled regex.')
    cls._resolution_validated = True

  @classmethod
  def _validate_resolution(cls):
    if cls._resolution_validated:
      return
    if not (cls._resolution is None or isinstance(cls._resolution, dict) or callable(cls._resolution)):
      raise Exception('_resolution must be None, function or a dictionary.')
    if isinstance(cls._resolution, dict):
      for synonym, func in cls._resolution.items():
        if not callable(func):
          raise Exception('Each value in _resolution should be a callable function.')
    cls._resolution_validated = True

  @classmethod
  def _validate_validation(cls):
    if cls._validation_validated:
      return
    if not (cls._validation is None or isinstance(cls._validation, dict) or callable(cls._validation)):
      raise Exception('_validation must be None, function or a dictionary.')
    if isinstance(cls._validation, dict):
      for synonym, func in cls._validation.items():
        if not callable(func):
          raise Exception('Each value in _validation should be a callable function.')
    cls._validation_validated = True

  @classmethod
  def consume(cls, query, start=0, end=None):
    cls._validate_rules()
    cls._validate_validation()
    matches = []

    if end is None:
      end = len(query)

    # Attempt to consume an identifier from query start. For each successful consumption, record the
    # (identifier, synonym_matching, matched_obj) tuple.
    for identifier, synonym_rules in cls._rules.items():
      for synonym_matching in synonym_rules:
        if isinstance(synonym_matching, str):
          synonym_matching = re.compile(synonym_matching, re.UNICODE)
        synonym_match_obj = synonym_matching.match(query, start, end)
        if synonym_match_obj is not None:
          valid = True
          if cls._validation is not None:
            if callable(cls._validation):
              valid = cls._validation(identifier, synonym_matching, synonym_match_obj)
            else:
              if synonym_matching in cls._validation:
                valid = cls._validation[synonym_matching](identifier, synonym_matching, synonym_match_obj)
          if valid:
            matches.append((identifier, synonym_matching, synonym_match_obj))

    return matches

  @classmethod
  def resolve(cls, identifier, synonym_matching, matched_obj, resl_func=None):
    cls._validate_resolution()
    if resl_func is not None:
      return resl_func(identifier, synonym_matching, matched_obj)
    if cls._resolution is None:
      return None
    if callable(cls._resolution):
      return cls._resolution(identifier, synonym_matching, matched_obj)
    if not synonym_matching in cls._resolution:
      return None
    return cls._resolution[synonym_matching](identifier, synonym_matching, matched_obj)
