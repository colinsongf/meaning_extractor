# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C11MeetingReservationQuery(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c11_meeting_reservation_query'

  _rules = {
    'reminder_query' : [
      '{date:st_date}',
      '{datetime:st_datetime}'
    ]
  }
