#!/usr/bin/python
# coding:utf-8

# kuaidi100 api
__author__ = 'Benny <benny@bennythink.com>'
__credits__ = 'ヨイツの賢狼ホロ <horo@yoitsu.moe>'

import json
import requests

import db
import utils
from com_dic import STATE, PROVIDER


def auto_detect(tracker):
    """
    auto detect express company
    :param tracker: ID
    :return: company name in pinyin
    """
    url = 'https://www.kuaidi100.com/autonumber/autoComNum?text=' + tracker
    result = requests.get(url).text

    try:
        r = json.loads(result).get('auto')[0].get('comCode')
        return r, PROVIDER.get(r, 'Default')
    except (IndexError, ValueError):
        return False, 'Default'


def query_express_status(com, track_id):
    """
    query express status
    :param com: company name in pinyin,
    :param track_id: id
    :return: the newest status
    """
    url = 'https://www.kuaidi100.com/query' + '?type=' + com + '&postid=' + track_id
    return json.loads(requests.get(url).text)


def recv(code, *args):
    """
    check if this track is done
    No result in database would return none, so do a query and insert
    :param code: express id
    :param args: usually Telegram message_id and chat_id(user_id)
    :return: message to be sent to the client
    """

    try:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))[0]
    except IndexError:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))

    if len(db_res) == 0:
        com_code, real_com_name = auto_detect(code)

        if not com_code:
            # TODO: Is it the pythonic way?
            return utils.reply_not_found()
        res = query_express_status(com_code, code)
        done = 1 if (res.get('state') == '3' or res.get('state') == '4') else 0

        try:
            sql_cmd = "INSERT INTO job VALUES (NULL ,?,?,?,?,?,?,?,?)"

            db.upsert(sql_cmd, (args[0], args[1], com_code, code, res.get('data')[0].get('context'),
                                STATE.get(res.get('state')), res.get('data')[0].get('time'), done))
            return code + ' ' + real_com_name + '\n' + res.get('data')[0].get('time') + ' ' + res.get('data')[0].get(
                'context')
        except IndexError:
            return res.get('message')
    elif db_res[8] == 0:
        com_code, real_com_name = auto_detect(code)

        if not com_code:
            # TODO: Is it the pythonic way?
            return utils.reply_not_found()
        res = query_express_status(com_code, code)
        done = 1 if (res.get('state') == '3' or res.get('state') == '4') else 0

        try:
            sql_cmd = "UPDATE job SET content=?,status=?,date=?,done=? WHERE track_id=?"

            db.upsert(sql_cmd, (res.get('data')[0].get('context'),
                                STATE.get(res.get('state')),
                                res.get('data')[0].get('time'),
                                done,
                                code))
            return code + ' ' + real_com_name + '\n' + res.get('data')[0].get('time') + ' ' + res.get('data')[0].get(
                'context')
        except IndexError:
            return res.get('message')
    else:
        return db_res[4] + ' ' + PROVIDER.get(db_res[3], 'Default') + '\n' + db_res[7] + ' ' + db_res[5]


def list_query(un):
    """
    list known user's info from database
    :param un: chat_id(user_id)
    :return: a list contains results.
    """
    cmd = "SELECT track_id,type,date,content FROM job WHERE chat_id=?"
    r = db.select(cmd, (un,))
    if len(r) == 0:
        return None
    else:
        r_tmp = []
        for i in r:
            tmp = list(i)
            tmp[1] = PROVIDER.get(tmp[1], 'Default')
            r_tmp.append(tmp)

        return r_tmp


def delete(tid):
    """
    delete a track record
    :param tid: express id
    :return: delete result, success or fail
    """
    cmd = "DELETE FROM job WHERE track_id=?"
    if db.upsert(cmd, (tid,)) == 1:
        return '删除成功 😋'
    else:
        return '那个在哪？'


if __name__ == '__main__':
    pass
