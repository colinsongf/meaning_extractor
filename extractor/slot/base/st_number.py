# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.utility.number import regex_number, chinese2num

class STNumber(Base):

  _slot_type_identifier = 'st_number'

  _rules = {
    'number' : [r'{}+'.format(regex_number)]
  }

  _resolve_base = lambda identifier, synonym_matching, match_obj : chinese2num(match_obj.group(0))
