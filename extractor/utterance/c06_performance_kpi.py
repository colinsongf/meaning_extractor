# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C06PerformanceKpi(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c06_performance_kpi'

  _rules = {
    'performance_kpi' : [
      '查(询){person:st_any}(的)[kpi|饱和度|工作饱和度]'
    ]
  }
