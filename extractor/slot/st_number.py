# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.utility.number import regex_number, chinese2num

import re

class STNumber(Base):

  def __regex_number_matchings():
    rtn = []
    for i in range(1, 16):
      regex = r'{}{{{}}}'.format(regex_number, i)
      rtn.append(re.compile(regex))
    return rtn

  def __validate_number(identifer, synonym_matching, matched_obj):
    try:
      chinese2num(matched_obj.group(0))
    except:
      return False
    return True

  _identifier = 'st_number'

  _rules = {
    'number' : __regex_number_matchings()
  }

  _validation = __validate_number

  _resolution = lambda identifier, synonym_matching, matched_obj : chinese2num(matched_obj.group(0))
