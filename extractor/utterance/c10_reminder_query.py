# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C10ReminderQuery(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c10_reminder_query'

  _rules = {
    'reminder_query' : [
      '{date:st_date}',
      '{datetime:st_datetime}'
    ]
  }
