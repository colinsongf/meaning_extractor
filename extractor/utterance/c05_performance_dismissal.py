# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C05PerformanceDismissal(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c05_performance_dismissal'

  _rules = {
    'performance_dismissal' : [
      '离职'
    ]
  }
