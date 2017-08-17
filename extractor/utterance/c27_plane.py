# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C27Plane(Utterance):

  _utterance_identifier = 'c27_plane'

  _rules = {
    'reservation' : ['[订|定]*({date:st_date})({time:st_time})*({city_from:st_city_chn}*{city_to:st_city_chn})*[航|机|票]']
  }
