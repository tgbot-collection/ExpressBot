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

c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())


def auto_detect(tracker):
    url = 'http://www.kuaidi100.com/autonumber/autoComNum?text=' + tracker
    com_result = StringIO.StringIO()

    try:
        c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, com_result.write)

        c.perform()

    except UnicodeEncodeError:
        pass

    try:
        return json.loads(com_result.getvalue()).get('auto')[0].get('comCode')
    except (IndexError, ValueError):
        return False


def query_express_status(com, track_id):
    url = 'http://www.kuaidi100.com/query'
    exp_result = StringIO.StringIO()

    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    c.setopt(pycurl.WRITEFUNCTION, exp_result.write)

    c.setopt(pycurl.URL, url + '?type=' + com + '&postid=' + track_id)
    c.perform()
    # return json.loads(s[s.index('}]}') + 3:])
    return json.loads(exp_result.getvalue())


def recv(code, *args):
    # check if this track is done
    # No result in database would return none, so do a query and insert

    # TODO: SQL Injection
    try:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))[0]
    except IndexError:
        db_res = db.select("SELECT * FROM job WHERE track_id=?", (code,))

    if len(db_res) == 0:
        com_code = auto_detect(code)

        if not com_code:
            return 'My dear, I think you have entered a wrong number.'
        res = query_express_status(com_code, code)
        done = 1 if (res.get('state') == '3' or res.get('state') == '4') else 0

        try:
            sql_cmd = "INSERT INTO job VALUES (NULL ,?,?,?,?,?,?,?,?)"

            db.upsert(sql_cmd, (args[0], args[1], com_code, code, res.get('data')[0].get('context'),
                                state.get(res.get('state')), res.get('data')[0].get('time'), done))
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
            sql_cmd = "UPDATE job SET content=?,status=?,date=?,done=? WHERE track_id=?"

            db.upsert(sql_cmd, (res.get('data')[0].get('context'),
                                state.get(res.get('state')),
                                res.get('data')[0].get('time'),
                                done,
                                code))
            return code + '\n' + res.get('data')[0].get('time') + ' ' + res.get('data')[0].get('context')
        except IndexError:
            return res.get('message')
    else:
        return db_res[4] + '\n' + db_res[7] + ' ' + db_res[5]


# TODO: what if the user has no history, it must say something.
def list_query(un):
    cmd = "SELECT track_id,date,content FROM job WHERE username=?"
    return db.select(cmd, (un,))


def delete(tid):
    cmd = "DELETE FROM job WHERE track_id=?"
    if db.upsert(cmd, (tid,)) == 1:
        return 'Delete succeed'
    else:
        return 'The ID you entered is not available.'


if __name__ == '__main__':
    print recv('***REMOVED***', 'BennyThink', 260260121)
    print recv('***REMOVED***', 'BennyThink', 260260121)
    print recv('***REMOVED***', 'BennyThink', 260260121)

    # delete('***REMOVED***')
