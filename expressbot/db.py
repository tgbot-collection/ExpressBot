#!/usr/bin/python
# coding:utf-8

# database connection

import sqlite3
import os

import config

DB_PATH = os.environ.get('DB_PATH') or config.DB_PATH

con = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = con.cursor()
create_table = '''CREATE TABLE IF NOT EXISTS job
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id VARCHAR(20),
    chat_id VARCHAR(20),
    type VARCHAR(20),
    track_id VARCHAR(20),
    content TEXT,
    status VARCHAR(10),
    date DATETIME,
    done TINYINT
)'''

cur.execute(create_table)
con.commit()


def upsert(cmd, param):
    cur.execute(cmd, param)
    con.commit()
    return cur.rowcount


def select(cmd, param):
    cur.execute(cmd, param)
    return cur.fetchall()
