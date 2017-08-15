# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class SampleUtterance1(Utterance):

  _utterance_identifier = 'sample_utterance_1'

  _rules = {
    'reservation' : ['{time:st_datetime}*({num_people:st_number}人)(的)(({room_loc:st_any})(号)[会议室|房间|办公室])']
  }
