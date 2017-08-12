"""from extractor.utility.number import num2chinese, chinese2num, regex_number
from extractor.slot.aggregate import Aggregate
import re

# print(regex_number.match('两百三'))
# print(arabic_cn_number_mapping(0, 100, True, twoalt=True))
# print(num2chinese(2000, o=False, twoalt=False))
print(Aggregate._standardize_expression('预定明天三点{timestamp:type_datetime}{num_people:type_people}的会议室'))
# for t in STNumber.consume('两百三十五'):
#   print(t)
#   print(STNumber.resolve(*t))
"""

# class A:
#   __a = 3

#   @classmethod
#   def p(cls):
#     print(cls.__a)

# class B(A):
#   pass

# B.p()

from extractor.slot.base.st_number import STNumber
from extractor.slot.aggregate.st_date import STDate
from extractor.slot.aggregate.st_time import STTime
from extractor.slot.aggregate import Aggregate
from extractor.utility.number import chinese2num

# for a, b in Aggregate._standardize_and_expand_rule('({am_pm:st_am_pm}){hour:st_number}[点|时]({minute:st_number}分({second:st_number}秒))'):
#   print(a)
#   print(b)
#   print('')

for t in STTime.consume('凌晨三点过三十分', greedy=True):
  print(str(t))

for t in STDate.consume('10号', greedy=True):
  print(str(t))


# print(chinese2num('下午三'))
