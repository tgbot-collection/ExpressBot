#!/usr/bin/python
# coding:utf-8

# ExpressBot - broadcast.py
# 2018/1/29 11:51
# TODO: need fix

__author__ = 'Benny <benny@bennythink.com>'

import db
import os
import sys
import time

import telebot

import config

TOKEN = os.environ.get('TOKEN') or config.TOKEN
DB_PATH = os.environ.get('DB_PATH') or config.DB_PATH


def broadcast(msg):
    bot = telebot.TeleBot(TOKEN)
    cmd = 'SELECT DISTINCT chat_id FROM job'
    user_list = db.select(cmd, '')

    for chat_id in user_list:
        bot.send_message(chat_id[0], msg)
        time.sleep(0.1)


def get_undone_count():
    cmd = 'SELECT * FROM job WHERE done=?'
    user_list = db.select(cmd, (0,))

    print('The undone job count is %s' % len(user_list))


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('参数错误')
    elif sys.argv[1] == '0':
        get_undone_count()
    else:
        # running under windows needs decode('gbk')
        broadcast(sys.argv[1])
