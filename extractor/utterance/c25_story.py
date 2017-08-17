# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C25Story(Utterance):

  _utterance_identifier = 'c25_story'

  _rules = {
    'story' : [
      '故事'
    ]
  }
