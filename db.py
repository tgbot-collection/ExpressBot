#!/usr/bin/python
# coding:utf-8


import sqlite3

con = sqlite3.connect('bot.db', check_same_thread=False)
cur = con.cursor()
cmd = '''CREATE TABLE IF NOT EXISTS job
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20),
    chat_id VARCHAR(20),
    type VARCHAR(20),
    track_id VARCHAR(20),
    content TEXT,
    status VARCHAR(10),
    date DATETIME,
    done BOOLEAN
)'''
cur.execute(cmd)
con.commit()


def upsert(cmd):
    # print cmd
    cur.execute(cmd)
    con.commit()


def select(cmd):
    cur.execute(cmd)
    return cur.fetchone()


def delete():
    pass
