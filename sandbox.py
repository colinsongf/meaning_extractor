from extractor.slot.base.st_number import STNumber
from extractor.slot.aggregate.st_date import STDate
from extractor.slot.aggregate.st_datetime import STDateTime
from extractor.slot.aggregate.st_time import STTime
from extractor.slot.aggregate import Aggregate
from extractor.utility.number import chinese2num

# for t in STTime.consume('凌晨三点过三十分三十分', greedy=True):
#   print(str(t))

# for t in STDate.consume('10号', greedy=True):
#   print(str(t))

for t in STDateTime.consume('10号二十点八分', greedy=True):
  print(str(t))
