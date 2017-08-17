# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C23Stock(Utterance):

  _utterance_identifier = 'c23_stock'

  _rules = {
    'stock' : [
      '([查|查询|调出]){stock_name:st_any}(的)股'
    ]
  }
