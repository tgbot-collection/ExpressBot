#!/usr/bin/python
# coding:utf-8

# ExpressBot - yyets_test.py
# 2018/2/12 11:48
# 

author = 'Benny <benny@bennythink.com>'

import os
import sys

sys.path.append(os.getcwd())
from expressbot import yyets

assert u'The.Flash.S03E18' in yyets.get_tv_link('闪电侠 3 18')
assert u'逃避' in yyets.query_resource('/query 逃避')
