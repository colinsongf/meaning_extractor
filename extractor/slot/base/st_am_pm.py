# -*- coding: utf-8 -*-

from extractor.slot.base import Base
from extractor.utility.number import regex_number, chinese2num

from datetime import datetime, date, time, timedelta

class STAmPm(Base):

  _slot_type_identifier = 'st_am_pm'

  _rules = {
    'am_tod' : ['早上', '上午', '今早', '凌晨'],
    'no_tod' : ['中午', '正午'],
    'pm_tod' : ['下午'],
    'ev_tod' : ['晚上', '今晚'],
    'mo_tom' : ['明早'],
    'no_tom' : ['明午'],
    'ev_tom' : ['明晚'],
    'mo_yes' : ['昨早'],
    'no_yes' : ['昨午'],
    'ev_yes' : ['昨晚'],
  }

  _resolve_base = lambda identifier, synonym_matching, match_obj : STAmPm.__apply_am_pm_to_datetime(identifier)

  @staticmethod
  def __apply_am_pm_to_datetime(identifier):
    def apply_func(dttm):
      if 'tom' in identifier:
        dttm += timedelta(days=1)
      elif 'yes' in identifier:
        dttm -= timedelta(days=1)
      if ('pm' in identifier and 0 < dttm.hour < 12) or ('ev' in identifier and 4 < dttm.hour < 12):
        dttm += timedelta(hours=12)
      return dttm
    return apply_func
