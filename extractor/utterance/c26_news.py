# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C26News(Utterance):

  _utterance_identifier = 'c26_news'

  _rules = {
    'news' : [
      '新闻'
    ]
  }
