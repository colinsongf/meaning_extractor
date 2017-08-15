# -*- coding: utf-8 -*-

from extractor.slot.aggregate import Aggregate

from datetime import datetime, date, time, timedelta

class STTime(Aggregate):

  _slot_type_identifier = 'st_time'

  _rules = {
    'now' : ['现在'],
    'time_explicit' : ['({am_pm:st_am_pm}){hour:st_number}[点|点过|时]({minute:st_number}分({second:st_number}秒))'],
    'hour_whole' : ['({am_pm:st_am_pm}){hour:st_number}[点|时][整|钟]'],
    'hour_half' : ['({am_pm:st_am_pm}){hour:st_number}[点|时]半'],
    'hour_quarter_1' : ['({am_pm:st_am_pm}){hour:st_number}[点|时]一刻'],
    'hour_quarter_3' : ['({am_pm:st_am_pm}){hour:st_number}[点|时]三刻'],
  }

  _resolve_aggregate = {
    'now' : lambda *args: datetime.now(),
    'time_explicit' : lambda _0, _1, _2, end, consumed, mp: STTime.__time_from_hms(mp),
    'hour_whole' : lambda _0, _1, _2, end, consumed, mp: STTime.__time_from_hms(mp),
    'hour_half' : lambda _0, _1, _2, end, consumed, mp: STTime.__time_from_hms(mp, timedelta(minutes=30)),
    'hour_quarter_1' : lambda _0, _1, _2, end, consumed, mp: STTime.__time_from_hms(mp, timedelta(minutes=15)),
    'hour_quarter_3' : lambda _0, _1, _2, end, consumed, mp: STTime.__time_from_hms(mp, timedelta(minutes=45)),
  }

  @classmethod
  def __time_from_hms(cls, mp, offset=None):
    try:
      if offset is None:
        offset = timedelta(seconds=0)

      hour = mp['hour'].slot_value if 'hour' in mp else 0
      minute = mp['minute'].slot_value if 'minute' in mp else 0
      second = mp['second'].slot_value if 'second' in mp else 0
      dttm = datetime.combine(date.today(), time(hour, minute, second))
      if 'am_pm' in mp:
        dttm = mp['am_pm'].slot_value(dttm)
      else:
        if 0 < dttm.time().hour < 6:
          dttm += timedelta(hours=12)
      return dttm + offset
    except:
      return None
