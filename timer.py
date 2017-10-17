#!/usr/bin/python
# coding:utf-8

import db
import main

if __name__ == '__main__':

    sql_cmd = 'SELECT track_id,username,chat_id,content FROM job WHERE done=?'
    s = db.select(sql_cmd, (0,))

    for i in s:
        # print i[0], i[1], i[2], i[3]
        main.cron(i[0], i[1], i[2], i[3])
