# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.utility.number import regex_number, chinese2num

import re

class STNumber(Base):

  def __validate_number(identifer, synonym_matching, matched_obj):
    try:
      chinese2num(matched_obj.group(0))
    except:
      return False
    return True

  _slot_type_identifier = 'st_number'

  _rules = {
    'number' : [r'{}+'.format(regex_number)]
  }

  _resolve = lambda identifier, synonym_matching, matched_obj : chinese2num(matched_obj.group(0))
