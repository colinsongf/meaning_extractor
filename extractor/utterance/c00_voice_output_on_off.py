# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C00VoiceOutputOnOff(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c00_voice_output_on_off'

  _rules = {
    'off' : ['关'],
    'on' : ['开']
  }
