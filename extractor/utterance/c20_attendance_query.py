# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C20AttendanceQuery(Utterance):

  _utterance_identifier = 'c20_attendance_query'

  _rules = {
    'attendance_query' : [
      '([查|查询|调出])({date:st_date}){person:st_any}(的)[考|出]勤',
      '([查|查询|调出]){person:st_any}({date:st_date})(的)[考|出]勤',
    ]
  }
