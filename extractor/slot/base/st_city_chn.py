# -*- coding: utf-8 -*-

from extractor.slot.base import Base

class STCityCHN(Base):

  _slot_type_identifier = 'st_city_chn'

  _rules = {
    'shenzhen' : ['深圳'],
    'shanghai' : ['上海', '魔都'],
    'beijing' : ['北京', '帝都'],
    # TODO: ...
  }

  _resolve_base = lambda identifier, synonym_matching, match_obj : chinese2num(matched_obj.group(0))
