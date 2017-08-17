# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C03SendEmail(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c03_send_email'

  _rules = {
    'email_contact' : [
      '[发|写]*给{person:st_any}',
      '给{person:st_any}[发|写]',
    ]
  }
