#!/usr/bin/python
# coding:utf-8

# timer for cron
__author__ = 'Benny <benny@bennythink.com>'

import os
import random
import sqlite3
import time

import telebot

import config
import kuaidi100

TOKEN = os.environ.get('TOKEN') or config.TOKEN
DB_PATH = os.environ.get('DB_PATH') or config.DB_PATH

bot = telebot.TeleBot(TOKEN)


# TODO: Improve echo msg and params
@bot.message_handler()
def cron(code, mid, cid, db_content):
    """
    cron job process for timer.py
    :param code: express id
    :param mid: message id for reply_to_message
    :param cid: chat_id(a.k.a user_id)
    :param db_content: old express status in database
    :return: None
    """
    # cancel cron job.
    if len(s) > 80:
        return

    r = kuaidi100.recv(code, mid, cid)
    # suppress maximum 2000 queries
    if db_content not in r and r != u'非法访问:IP禁止访问':
        try:
            bot.send_message(chat_id=cid, reply_to_message_id=mid, text=r)
        except telebot.apihelper.ApiException as e:
            print(e.message)


def select(cmd):
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = con.cursor()

    cur.execute(cmd)
    data = cur.fetchall()
    con.close()
    return data


if __name__ == '__main__':
    sql_cmd = 'SELECT track_id,message_id,chat_id,content FROM job WHERE done=0'
    s = select(sql_cmd)
    delay = random.uniform(1, 4)

    for i in s:
        cron(i[0], i[1], i[2], i[3])
        time.sleep(delay)
