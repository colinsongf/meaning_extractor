# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C01PhoneCall(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c01_phone_call'

  _rules = {
    'phone_contact' : [
      '[打给|打电话给|查询|拨打|拨|呼叫]{person:st_any}',
      '[打|拨打|呼叫]{person:st_any}(的)[手机|电话]',
    ]
  }
