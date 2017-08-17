# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C09Reminder(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c09_reminder'

  _rules = {
    'reminder' : [
      '[提醒|告诉|让|叫]*{date:st_date}{content:st_any}',
      '[提醒|告诉|让|叫]*{datetime:st_datetime}{content:st_any}'
    ]
  }
