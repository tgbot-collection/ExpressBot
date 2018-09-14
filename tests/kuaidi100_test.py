#!/usr/bin/python
# coding:utf-8

# ExpressBot - kuaidi100_test.py
# 2018/2/12 11:19
# 

author = 'Benny <benny@bennythink.com>'

import os
import sys

sys.path.append(os.getcwd())
from expressbot import kuaidi100

result = kuaidi100.receiver('100000', 0, 0)
assert result is not None

