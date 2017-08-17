# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C02SendMessage(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c02_send_message'

  _rules = {
    'phone_contact' : [
      '[发|写][信息|短信]给{person:st_any}',
      '给{person:st_any}[发|写][信息|短信]',
    ]
  }
