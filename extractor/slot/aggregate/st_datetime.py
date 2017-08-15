# -*- coding: utf-8 -*-

from extractor.slot.aggregate import Aggregate

from datetime import datetime, date, time, timedelta

import calendar

class STDateTime(Aggregate):

  _slot_type_identifier = 'st_datetime'

  _rules = {
    'datetime' : ['({date:st_date}){time:st_time}']
  }

  _resolve_aggregate = {
    'datetime' : lambda _0, _1, _2, end, consumed, mp: STDateTime.__datetime_func(mp)
  }

  @classmethod
  def __datetime_func(cls, mp):
    try:
      dttm = mp['time'].slot_value
      if 'date' in mp:
        dt = mp['date'].slot_value
        return datetime.combine(dt, dttm.time())
      return dttm
    except:
      return None
