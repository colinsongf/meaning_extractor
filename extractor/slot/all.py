# -*- coding: utf-8 -*-

from extractor.slot.st_number import STNumber

class Slot(object):

  __all_slot_cls = [STNumber]

  __all_slot_mapping = dict()

  @classmethod
  def with_identifier(cls, identifier):
    if cls.__all_slot_cls and not cls.__all_slot_mapping:
      for slot_cls in cls.__all_slot_cls:
        cls.__all_slot_mapping[slot_cls._identifier] = slot_cls
    assert identifier in cls.__all_slot_mapping
    return cls.__all_slot_mapping[identifier]
