#!/usr/bin/python
# coding:utf-8

# kuaidi100 api
__author__ = 'Benny <benny@bennythink.com>'
__credits__ = 'ヨイツの賢狼ホロ <horo@yoitsu.moe>'

import json
import requests
import time

import utils
from constants import PROVIDER
from config import INTERVAL
from db import Database


def __auto_detect(track_id):
    """
    auto detect express company
    :param track_id: ID
    :return: pinyin
    """
    url = 'https://www.kuaidi100.com/autonumber/autoComNum?text=' + track_id
    result = requests.get(url).text

    try:
        r = json.loads(result).get('auto')[0].get('comCode')
        return r
    except (IndexError, ValueError):
        return None


def __query_status(track_id):
    """
    query express status
    :param track_id: id
    :return: json
    """
    company_name = __auto_detect(track_id)

    url = 'https://www.kuaidi100.com/query' + '?type=' + company_name + '&postid=' + track_id
    result = json.loads(requests.get(url).text)
    return result


def receiver(track_id, *args):
    """
    check if this track is done
    No result in database would return none, so do a query and insert
    :param track_id: express id
    :param args: usually Telegram message_id and chat_id(user_id)
    :return: message to be sent to the client
    """
    # 1. query from database
    # 2. older or none, query kuaidi100, update database
    # 3. return status result

    db = Database()
    data = db.retrieve({'track_id': track_id})
    try:
        db_time = float(data[0][6])
    except IndexError:
        db_time = 0

    r = utils.reply_refuse()
    try:
        r = __doing_query(db_time, track_id, args, data)
    except Exception as e:
        print(e)
    finally:

        return r


def __doing_query(db_time, track_id, args, data):
    if time.time() - db_time <= INTERVAL * 60:
        # print('just store')
        return data[0][5]
    elif len(data) == 0:
        # print('insert now')
        res = __query_status(track_id)

        if res['status'] != '200':
            return res['message']
        else:
            p = (args[0], args[1], PROVIDER.get(res['com']), track_id, res['data'][0]['context'],
                 int(time.time()), __process_status(res['state']))
            Database().create(p)

        return res['data'][0]['context']
    else:
        # print('update and save')
        res = __query_status(track_id)

        if res['status'] != '200':
            return res['message']
        else:
            p = (res['data'][0]['context'], int(time.time()), __process_status(res['state']), track_id)
            Database().update(p)

        return res['data'][0]['context']


def __process_status(code):
    c = 1 if code == '3' or code == '1' else 0
    return c


def __store_result(a):
    db = Database()
    db.create(a)


def list_query(_id):
    return Database().retrieve({'chat_id': _id})


def delete_record(track_id):
    count = Database().delete(track_id)
    return '删除成功' if count else '那个在哪？'


if __name__ == '__main__':
    print(receiver('263432466781', '260130', '941226'))
    print(list_query(941226))
