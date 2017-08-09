#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import math
import re

def num2chinese(num, big=False, simp=True, o=False, twoalt=False):
  """
  From: https://gist.github.com/gumblex/0d65cad2ba607fd14de7
  Converts numbers to Chinese representations.
  `big`   : use financial characters.
  `simp`  : use simplified characters instead of traditional characters.
  `o`     : use 〇 for zero.
  `twoalt`: use 两/兩 for two when appropriate.
  Note that `o` and `twoalt` is ignored when `big` is used,
  and `twoalt` is ignored when `o` is used for formal representations.
  """
  # check num first
  nd = str(num)
  if abs(float(nd)) >= 1e48:
    raise ValueError('number out of range')
  elif 'e' in nd:
    raise ValueError('scientific notation is not supported')
  c_symbol = '正负点' if simp else '正負點'
  if o:  # formal
    twoalt = False
  if big:
    c_basic = '零壹贰叁肆伍陆柒捌玖' if simp else '零壹貳參肆伍陸柒捌玖'
    c_unit1 = '拾佰仟'
    c_twoalt = '贰' if simp else '貳'
  else:
    c_basic = '〇一二三四五六七八九' if o else '零一二三四五六七八九'
    c_unit1 = '十百千'
    if twoalt:
      c_twoalt = '两' if simp else '兩'
    else:
      c_twoalt = '二'
  c_unit2 = '万亿兆京垓秭穰沟涧正载' if simp else '萬億兆京垓秭穰溝澗正載'
  revuniq = lambda l: ''.join(k for k, g in itertools.groupby(reversed(l)))
  nd = str(num)
  result = []
  if nd[0] == '+':
    result.append(c_symbol[0])
  elif nd[0] == '-':
    result.append(c_symbol[1])
  if '.' in nd:
    integer, remainder = nd.lstrip('+-').split('.')
  else:
    integer, remainder = nd.lstrip('+-'), None
  if int(integer):
    splitted = [integer[max(i - 4, 0):i]
          for i in range(len(integer), 0, -4)]
    intresult = []
    for nu, unit in enumerate(splitted):
      # special cases
      if int(unit) == 0:  # 0000
        intresult.append(c_basic[0])
        continue
      elif nu > 0 and int(unit) == 2:  # 0002
        intresult.append(c_twoalt + c_unit2[nu - 1])
        continue
      ulist = []
      unit = unit.zfill(4)
      for nc, ch in enumerate(reversed(unit)):
        if ch == '0':
          if ulist:  # ???0
            ulist.append(c_basic[0])
        elif nc == 0:
          ulist.append(c_basic[int(ch)])
        elif nc == 1 and ch == '1' and unit[1] == '0':
          # special case for tens
          # edit the 'elif' if you don't like
          # 十四, 三千零十四, 三千三百一十四
          ulist.append(c_unit1[0])
        elif nc > 1 and ch == '2':
          ulist.append(c_twoalt + c_unit1[nc - 1])
        else:
          ulist.append(c_basic[int(ch)] + c_unit1[nc - 1])
      ustr = revuniq(ulist)
      if nu == 0:
        intresult.append(ustr)
      else:
        intresult.append(ustr + c_unit2[nu - 1])
    result.append(revuniq(intresult).strip(c_basic[0]))
  else:
    result.append(c_basic[0])
  if remainder:
    result.append(c_symbol[2])
    result.append(''.join(c_basic[int(ch)] for ch in remainder))
  return ''.join(result)

# author: binux(17175297.hk@gmail.com)
# Modified from https://binux.blog/2011/03/python-tools-chinese-digit/
conversion = {'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000,
       '０':0, '１':1, '２':2, '３':3, '４':4, '５':5, '６':6, '７':7, '８':8, '９':9,
                '壹':1, '贰':2, '叁':3, '肆':4, '伍':5, '陆':6, '柒':7, '捌':8, '玖':9, '拾':10, '佰':100, '仟':1000, '萬':10000,
       '亿':100000000}
def chinese2num(a):
  count = 0
  result = 0
  tmp = 0
  billion = 0
  if len(a) >= 3:
    if a[-2] in '百千万' and a[-1] in '一二三四五六七八九':
      base_power = conversion.get(a[-2], 0)
      return int(chinese2num(a[:-1]) + conversion.get(a[2], 0) * base_power / 10)
  while count < len(a):
    tmpChr = a[count]
    #print tmpChr
    tmpNum = conversion.get(tmpChr, None)
    if tmpNum is None:
      raise Exception('Invalid number format.')
    #如果等于1亿
    if tmpNum == 100000000:
      result = result + tmp
      result = result * tmpNum
      #获得亿以上的数量，将其保存在中间变量billion中并清空result
      billion = billion * 100000000 + result
      result = 0
      tmp = 0
    #如果等于1万
    elif tmpNum == 10000:
      result = result + tmp
      result = result * tmpNum
      tmp = 0
    #如果等于十或者百，千
    elif tmpNum >= 10:
      if tmp == 0:
        tmp = 1
      result = result + tmpNum * tmp
      tmp = 0
    #如果是个位数
    elif tmpNum is not None:
      tmp = tmp * 10 + tmpNum
    count += 1
  # if result > 0:
  #   result = result + tmp * 10 ** (int(math.log(result, 10)) - 1)
  # else:
  result += tmp
  result = result + billion
  return result

regex_number = r'[0-9０１２３４５６７８９〇一二两兩三四五六七八九十百千万亿兆零壹贰叁肆伍陆柒捌玖拾佰仟萬億兆]'
