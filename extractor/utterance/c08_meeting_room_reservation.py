# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C08MeetingRoomReservation(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c08_meeting_room_reservation'

  _rules = {
    'reservation' : [
      '[订|定]*({time:st_datetime})*({num_people:st_number}人)(的)(({room_loc:st_any})(号)[会议室|房间|办公室])({duration:st_number}小时)',
      ]
  }
