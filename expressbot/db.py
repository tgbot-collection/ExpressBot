#!/usr/bin/python
# coding:utf-8

# database connection


import sqlite3

from config import DB_PATH


class Database:

    def __init__(self):
        self.con = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.init_db()

    def __del__(self):
        self.con.close()

    def init_db(self):
        cur = self.con.cursor()
        job = '''
        CREATE TABLE IF NOT EXISTS job
    (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      message_id VARCHAR(20),
      chat_id    VARCHAR(20),
      company       VARCHAR(20),
      track_id   VARCHAR(20),
      content    TEXT,
      timestamp     INT,
      done       BOOLEAN
    )
        '''
        msg = '''
        CREATE TABLE IF NOT EXISTS msg
    (
      ID       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      user_id  VARCHAR(10),
      message_id  VARCHAR(10),
      username VARCHAR(20),
      realname VARCHAR(30),
      chat     TEXT,
      time     DATETIME
    )
        '''
        cur.execute(msg)
        cur.execute(job)
        self.con.commit()

    def run_query(self, cmd, param):
        cur = self.con.cursor()
        cur.execute(cmd, param)
        result, count = cur.fetchall(), cur.rowcount
        self.con.commit()
        self.con.close()
        return result, count

    def create(self, param):
        sql_cmd = "INSERT INTO job VALUES (NULL ,?,?,?,?,?,?,?)"
        self.run_query(sql_cmd, param)

    def retrieve(self, param=None):
        # param could be: track_id, chat_id, done
        if param.get('track_id'):
            sql_cmd = "SELECT * FROM job WHERE track_id=?"
            p = param.get('track_id')
        elif param.get('chat_id'):
            sql_cmd = "SELECT * FROM job WHERE chat_id=?"
            p = param.get('chat_id')
        elif param.get('done'):
            p = param.get('done')
            sql_cmd = "SELECT * FROM job WHERE done=?"
        else:
            return

        data, _ = self.run_query(sql_cmd, (p,))
        return data

    def update(self, param):
        sql_cmd = "UPDATE job SET content=?,`timestamp`=?,done=? WHERE track_id=?"
        self.run_query(sql_cmd, param)

    def delete(self, param):
        sql_cmd = "DELETE FROM job WHERE track_id=?"
        _, count = self.run_query(sql_cmd, (param,))
        return count


if __name__ == '__main__':
    Database().init_db()
