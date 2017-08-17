# -*- coding: utf-8 -*-

from extractor.utterance import Utterance

class C07VisitWebsite(Utterance):
  # Meeting reservation

  _utterance_identifier = 'c07_visit_website'

  _rules = {
    'visit_website' : [
      '[上|访问|搜索|打开|浏览]{website_name:st_any}([网|网站|网页|网址])',
    ]
  }
