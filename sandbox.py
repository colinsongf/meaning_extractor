from extractor.utility.number import num2chinese, chinese2num, regex_number
from extractor.slot.aggregate import Aggregate
from extractor.slot.st_number import STNumber
import re

# print(regex_number.match('两百三'))
# print(arabic_cn_number_mapping(0, 100, True, twoalt=True))
# print(num2chinese(2000, o=False, twoalt=False))
print(Aggregate._standardize_expression('预定明天三点{timestamp:type_datetime}{num_people:type_people}的会议室'))
# for t in STNumber.consume('两百三十五'):
#   print(t)
#   print(STNumber.resolve(*t))
