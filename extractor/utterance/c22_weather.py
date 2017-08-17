# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C22Weather(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c22_weather'

  _rules = {
    'weather' : [
      '({date:st_date})*({city:st_city_chn})',
      '({city:st_city_chn})*{date:st_date}',
      '({datetime:st_datetime})*({city:st_city_chn})',
      '({city:st_city_chn})*{datetime:st_datetime}',
    ],
  }
