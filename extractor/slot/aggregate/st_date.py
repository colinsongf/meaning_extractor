# -*- coding: utf-8 -*-

from extractor.slot.aggregate import Aggregate

from datetime import datetime, date, time, timedelta

import calendar

class STDate(Aggregate):

  _slot_type_identifier = 'st_date'

  _rules = {
    '0' : ['今天'],
    '+1' : ['明天'],
    '+2' : ['后天'],
    '-1' : ['昨天'],
    '-2' : ['前天'],
    '-7' : ['上(个)[周|星期]'],
    '+7' : ['下(个)[周|星期]'],
    '-30' : ['上(个)[月|月份]'],
    '+30' : ['下(个)[月|月份]'],
    'day_of_this_week' : ['[这|本|][周|星期][一|二|三|四|五|六|七|天|日]'],
    'day_of_last_week' : ['上[周|星期][一|二|三|四|五|六|七|天|日]'],
    'day_of_next_week' : ['下[周|星期][一|二|三|四|五|六|七|天|日]'],
    'day_explicit' : ['({year:st_number}年)({month:st_number}月)({day:st_number}[日|号])']
  }

  _resolve_aggregate = {
    '0' :  lambda *args: date.today(),
    '+1' : lambda *args: date.today() + timedelta(days=1),
    '+2' : lambda *args: date.today() + timedelta(days=2),
    '+7' : lambda *args: date.today() + timedelta(days=7),
    '+30' : lambda *args: date.today() - timedelta(days=30),
    '-1' : lambda *args: date.today() - timedelta(days=1),
    '-2' : lambda *args: date.today() - timedelta(days=2),
    '-7' : lambda *args: date.today() - timedelta(days=7),
    '-30' : lambda *args: date.today() - timedelta(days=30),
    'day_of_this_week' : lambda _0, _1, _2, end, consumed, mp: STDate.__day_of_week_func(consumed, 0),
    'day_of_last_week' : lambda _0, _1, _2, end, consumed, mp: STDate.__day_of_week_func(consumed, -1),
    'day_of_next_week' : lambda _0, _1, _2, end, consumed, mp: STDate.__day_of_week_func(consumed, 1),
    'day_explicit' : lambda _0, _1, _2, end, consumed, mp: STDate.__date_from_year_ymd(mp),
  }

  __day_mapping = {
    '一' : calendar.MONDAY,
    '二' : calendar.TUESDAY,
    '三' : calendar.WEDNESDAY,
    '四' : calendar.THURSDAY,
    '五' : calendar.FRIDAY,
    '六' : calendar.SATURDAY,
    '七' : calendar.SUNDAY,
    '天' : calendar.SUNDAY,
    '日' : calendar.SUNDAY,
  }

  @classmethod
  def __day_of_week_func(cls, consumed, week_delta):
    today = date.today()
    one_week = timedelta(days=7)
    target_weekday = cls.__day_mapping[consumed[-1]]
    today_weekday = today.weekday()
    tentative = today + timedelta((target_weekday - today_weekday) % 7)
    if today_weekday <= target_weekday:
      return tentative + week_delta * one_week
    else:
      return tentative + (week_delta - 1) * one_week

  @classmethod
  def __date_from_year_ymd(cls, mp):
    try:
      dt = date.today()
      if 'year' in mp:
        dt = dt.replace(year=mp['year'].slot_value)
      if 'month' in mp:
        dt = dt.replace(month=mp['month'].slot_value)
      if 'day' in mp:
        dt = dt.replace(day=mp['day'].slot_value)
      return dt
    except:
      return None
