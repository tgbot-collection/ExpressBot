#!/usr/bin/python
# coding:utf-8


import sqlite3

con = sqlite3.connect('bot.db', check_same_thread=False)
cur = con.cursor()


def upsert(cmd):
    # print cmd
    cur.execute(cmd)
    con.commit()


def select(cmd):
    cur.execute(cmd)
    return cur.fetchone()


def delete():
    pass
