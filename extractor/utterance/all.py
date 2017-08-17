# -*- coding: utf-8 -*-

from extractor.utterance.c00_voice_output_on_off import C00VoiceOutputOnOff
from extractor.utterance.c01_phone_call import C01PhoneCall
from extractor.utterance.c02_send_message import C02SendMessage
from extractor.utterance.c03_send_email import C03SendEmail
from extractor.utterance.c04_navigation import C04Navigation
from extractor.utterance.c05_performance_dismissal import C05PerformanceDismissal
from extractor.utterance.c06_performance_kpi import C06PerformanceKpi
from extractor.utterance.c07_visit_website import C07VisitWebsite
from extractor.utterance.c08_meeting_room_reservation import C08MeetingRoomReservation
from extractor.utterance.c09_reminder import C09Reminder
from extractor.utterance.c10_reminder_query import C10ReminderQuery
from extractor.utterance.c11_meeting_reservation_query import C11MeetingReservationQuery
from extractor.utterance.c20_attendance_query import C20AttendanceQuery
from extractor.utterance.c21_business_trip_query import C21BusinessTripQuery
from extractor.utterance.c22_weather import C22Weather
from extractor.utterance.c23_stock import C23Stock
from extractor.utterance.c24_joke import C24Joke
from extractor.utterance.c25_story import C25Story
from extractor.utterance.c26_news import C26News
from extractor.utterance.c27_plane import C27Plane
from extractor.utterance.c28_train import C28Train

class UtteranceAll(object):

  __all_utterance_mapping = {
    0 : C00VoiceOutputOnOff,
    1 : C01PhoneCall,
    2 : C02SendMessage,
    3 : C03SendEmail,
    4 : C04Navigation,
    5 : C05PerformanceDismissal,
    6 : C06PerformanceKpi,
    7 : C07VisitWebsite,
    8 : C08MeetingRoomReservation,
    9 : C09Reminder,
    10 : C10ReminderQuery,
    11 : C11MeetingReservationQuery,
    20 : C20AttendanceQuery,
    21 : C21BusinessTripQuery,
    22 : C22Weather,
    23 : C23Stock,
    24 : C24Joke,
    25 : C25Story,
    26 : C26News,
    27 : C27Plane,
    28 : C28Train,
  }

  @classmethod
  def with_category(cls, category):
    if category in cls.__all_utterance_mapping:
      return cls.__all_utterance_mapping[category]
    return None
