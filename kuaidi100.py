#!/usr/bin/python
# coding:utf-8

import pycurl
import certifi
import StringIO
import json
import db
from dec import STATE, PROVIDER

# 0	Transporting	Express is being transported
# 1	Accepted	Express is accepted by the express company
# 2	Trouble	Express is in knotty problem
# 3	Delivered	Express is successfully delivered
# 4	Rejected	Express is rejected by the receiver and has been successfully redelivered to the sender
# 5	Delivering	Express is being delivered
# 6	Rejecting	Express is rejected by the receiver and is being redelivered to the sender


c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())


def auto_detect(tracker):
    url = 'https://www.kuaidi100.com/autonumber/autoComNum?text=' + tracker
    com_result = StringIO.StringIO()

    try:
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, com_result.write)
        c.perform()
    except UnicodeEncodeError, pycurl.error:
        pass

    try:
        r = json.loads(com_result.getvalue()).get('auto')[0].get('comCode')
        return r, PROVIDER.get(r, 'Default')
    except (IndexError, ValueError):
        return False, 'Default'


def query_express_status(com, track_id):
    url = 'https://www.kuaidi100.com/query' + '?type=' + com + '&postid=' + track_id
    exp_result = StringIO.StringIO()

    try:
        c.setopt(pycurl.CUSTOMREQUEST, 'GET')
        c.setopt(pycurl.WRITEFUNCTION, exp_result.write)
        c.setopt(pycurl.URL, url)
        c.perform()
        # return json.loads(s[s.index('}]}') + 3:])
        return json.loads(exp_result.getvalue())
    except pycurl.error:
        pass


def recv(code, *args):
    # check if this track is done
    # No result in database would return none, so do a query and insert

    # TODO: SQL Injection
    try:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))[0]
    except IndexError:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))

    if len(db_res) == 0:
        com_code, real_com_name = auto_detect(code)

        if not com_code:
            return '亲爱的，我感觉你仿佛在刻意逗我笑~ o(*￣▽￣*)o'
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
            return '亲爱的，我感觉你仿佛在刻意逗我笑~ o(*￣▽￣*)o'
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


# TODO: Logic process could not be done in here, cause we need send message separately
# for quick del
# TODO: OMG, just send one message instead...
def list_query(un):
    cmd = "SELECT track_id,type,date,content FROM job WHERE chat_id=?"
    r = db.select(cmd, (un,))
    if len(r) == 0:
        return None
    else:

        test = []
        for i in r:
            tmp = list(i)
            tmp[1] = PROVIDER.get(tmp[1], 'Default')
            test.append(tmp)

        return test


def delete(tid):
    cmd = "DELETE FROM job WHERE track_id=?"
    if db.upsert(cmd, (tid,)) == 1:
        return '删除成功'
    else:
        return '你所输入的运单编号不存在呢哟'


if __name__ == '__main__':
    pass
