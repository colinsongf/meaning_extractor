# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C28Train(Utterance):

  _utterance_identifier = 'c28_train'

  _rules = {
    'reservation' : ['[订|定]*({date:st_date})({time:st_time})*({city_from:st_city_chn}*{city_to:st_city_chn})*[高铁|火车|动车]']
  }
