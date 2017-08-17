# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C21BusinessTripQuery(Utterance):

  _utterance_identifier = 'c21_business_trip_query'

  _rules = {
    'business_trip_query' : [
      '([查|查询|调出])({date:st_date}){person:st_any}(的)出差',
      '([查|查询|调出]){person:st_any}({date:st_date})(的)出差',
    ]
  }
