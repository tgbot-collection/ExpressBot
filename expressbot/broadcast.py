#!/usr/bin/python
# coding:utf-8

# ExpressBot - broadcast.py
# 2018/1/29 11:51
# 

__author__ = 'Benny <benny@bennythink.com>'

import db
import sys

from main import send_message


def broadcast(msg):
    cmd = 'SELECT DISTINCT chat_id FROM job'
    user_list = db.select(cmd, '')

    for chat_id in user_list:
        send_message(chat_id[0], msg)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('参数错误')
    else:
        # running under windows needs decode('gbk')
        broadcast(sys.argv[1])
