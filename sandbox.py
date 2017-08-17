from extractor.slot.base.st_number import STNumber
from extractor.slot.aggregate.st_date import STDate
from extractor.slot.aggregate.st_datetime import STDateTime
from extractor.slot.aggregate.st_time import STTime
from extractor.slot.aggregate import Aggregate
from extractor.utility.number import chinese2num
from extractor.utterance.all import UtteranceAll

# for t in STTime.consume('凌晨三点过三十分三十分', greedy=True):
#   print(str(t))

# for t in STDate.consume('10号', greedy=True):
#   print(str(t))

# for t in STDateTime.consume('明天下午三点', greedy=True):
#   print(str(t))

for t in UtteranceAll.with_category(22).match('明天下午三点会下雨嘛', exact_match=False):
  print('----------------------------')
  print('用户文本: {}'.format(t.query))
  # print('匹配表达式: {}'.format(t.raw_rule))
  # print('匹配展开表达式: {}'.format(t.matched_rule))
  print('匹配: {}'.format(t.rule_identifier))
  print('匹配区段: ({}, {})'.format(t.match_start, t.match_end))
  print('匹配区段原始值: {}'.format(t.query[t.match_start:t.match_end]))
  print('匹配槽:')
  for key, val in t.slot_mappings.items():
    print('  [{}] {} -> {}'.format(val.slot_type.__name__, key, val.slot_value))
  # print('匹配区间:')
  # for seg in t.match_segments:
  #   print('  {}'.format(seg))
  print('----------------------------')

# STTime._validate_and_standardize()
# for identifier, raw_rules in STTime._rules_standard.items():
#   print('=============')
#   print(identifier)
#   for (raw_rule, standardized_rules) in raw_rules:
#     print('-------------')
#     print(raw_rule)
#     print(standardized_rules)
#     print('-------------')
#   print('=============')

# import os
# for f in os.listdir('./extractor/utterance'):
#   if f.startswith('c'):
#     mod_name = f[:-3]
#     cls_name = ''.join((' '.join(mod_name.split('_'))).title().split(' '))
#     # print('from {} import {}'.format(mod_name, cls_name))
#     print('{} : {},'.format(int(mod_name[1:3]), cls_name))
