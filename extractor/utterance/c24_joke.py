# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C24Joke(Utterance):

  _utterance_identifier = 'c24_joke'

  _rules = {
    'joke' : [
      '笑话'
    ]
  }
