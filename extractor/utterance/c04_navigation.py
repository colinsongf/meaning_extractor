# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C04Navigation(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c04_navigation'

  _rules = {
    'navigation_exact_address' : [
      '(导航)*([去|到|至|往]){location:st_any}(去)(怎么走)'
    ]
  }
