#!/usr/bin/python
# coding:utf-8

# ExpressBot - msg.py
# 2017/12/21 14:35
# message msg_logger

__author__ = 'Benny <benny@bennythink.com>'

import sqlite3
import time

ENABLE = False
con = sqlite3.connect('logger.db', check_same_thread=False)
cur = con.cursor()
create_table = '''CREATE TABLE IF NOT EXISTS msg
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id VARCHAR(10),
    username VARCHAR(20),
    realname VARCHAR(30),
    chat TEXT,
    time DATETIME
)'''
cur.execute(create_table)


def msg_logger(fun):
    def wrapper(*args, **kwargs):
        res = fun(*args, **kwargs)
        if ENABLE:
            sql = 'INSERT INTO msg VALUES (NULL ,?,?,?,?,?)'
            # user
            cur.execute(sql, (
                args[0].chat.id, args[0].chat.username, args[0].chat.first_name + args[0].chat.last_name, args[0].text,
                time.ctime(args[0].date)))
            # bot
            cur.execute(sql, (0, 'bot', 'bot', res, time.ctime()))
            con.commit()
        return res

    return wrapper
