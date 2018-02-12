#!/usr/bin/python
# coding:utf-8

# ExpressBot - turing_test.py
# 2018/2/12 10:58
# 

author = 'Benny <benny@bennythink.com>'

import os
import sys

sys.path.append(os.getcwd())
from expressbot import turing

result = turing.send_turing(os.environ.get('TURING_KEY'), '你是谁', 0)
assert u'小明' in result
