#!/usr/bin/python
# coding:utf-8

import pycurl
import certifi
import StringIO
import json
import db

# 0	Transporting	Express is being transported
# 1	Accepted	Express is accepted by the express company
# 2	Trouble	Express is in knotty problem
# 3	Delivered	Express is successfully delivered
# 4	Rejected	Express is rejected by the receiver and has been successfully redelivered to the sender
# 5	Delivering	Express is being delivered
# 6	Rejecting	Express is rejected by the receiver and is being redelivered to the sender

state = {'0': 'Transporting', '1': 'Accepted', '2': 'Trouble', '3': 'Delivered', '4': 'Rejected', '5': 'Delivering',
         '6': 'Rejecting'}

result = StringIO.StringIO()

c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())
c.setopt(pycurl.WRITEFUNCTION, result.write)


def auto_detect(track_id):
    url = 'http://www.kuaidi100.com/autonumber/autoComNum'
    c.setopt(pycurl.CUSTOMREQUEST, 'POST')
    try:
        c.setopt(pycurl.URL, url + '?text=' + track_id)
        c.perform()
    except UnicodeEncodeError:
        pass

    try:
        return json.loads(result.getvalue()).get('auto')[0].get('comCode')
    except (IndexError, ValueError):
        return False


def query_express_status(com, track_id):
    url = 'http://www.kuaidi100.com/query'
    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    c.setopt(pycurl.URL, url + '?type=' + com + '&postid=' + track_id)
    c.perform()
    s = result.getvalue()
    return json.loads(s[s.index('}]}') + 3:])


def recv(code, *args):
    # check if this track is done
    # No result in database would return none, so do a query and insert

    # TODO: SQL Injection
    try:
        db_res = db.select("SELECT * FROM job WHERE track_id='%s'" % code)[0]
    except IndexError:
        db_res = db.select("SELECT * FROM job WHERE track_id='%s'" % code)

    if len(db_res) == 0:
        com_code = auto_detect(code)
        if not com_code:
            return 'My dear, I think you have entered a wrong number.'
        res = query_express_status(com_code, code)

        done = 1 if (res.get('state') == '3' or res.get('state') == '4') else 0
        try:
            sql_cmd = "INSERT INTO job VALUES (%s,'%s','%s','%s','%s','%s','%s','%s','%s')" % \
                      ('null', args[0], args[1], com_code, code, res.get('data')[0].get('context'),
                       state.get(res.get('state')), res.get('data')[0].get('time'), done)

            db.upsert(sql_cmd)
            return code + '\n' + res.get('data')[0].get('time') + ' ' + res.get('data')[0].get('context')
        except IndexError:
            return res.get('message')
    elif db_res[8] == 0:
        com_code = auto_detect(code)
        if not com_code:
            return 'My dear, I think you have entered a wrong number.'
        res = query_express_status(com_code, code)
        done = 1 if (res.get('state') == '3' or res.get('state') == '4') else 0
        try:
            sql_cmd = "UPDATE job set content='%s',status='%s',date='%s',done='%s' WHERE track_id='%s'" % \
                      (res.get('data')[0].get('context'),
                       state.get(res.get('state')),
                       res.get('data')[0].get('time'),
                       done,
                       code)
            db.upsert(sql_cmd)
            return code + '\n' + res.get('data')[0].get('time') + ' ' + res.get('data')[0].get('context')
        except IndexError:
            return res.get('message')
    else:
        return db_res[4] + '\n' + db_res[7] + ' ' + db_res[5]


def list_query(un):
    cmd = "SELECT track_id,date,content FROM job WHERE username='%s'" % un
    return db.select(cmd)


def delete(tid):
    cmd = "DELETE FROM job WHERE track_id='%s'" % tid
    if db.upsert(cmd) == 1:
        return 'Delete succeed'
    else:
        return 'The ID you entered is not available.'


if __name__ == '__main__':
    print recv('***REMOVED***', 'BennyThink', 260260121)
    # print recv('***REMOVED***', 'BennyThink', 260260121)
    # list_query('BennyThink')
    # delete('***REMOVED***')
