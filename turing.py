#!/usr/bin/python
# coding:utf-8


import pycurl
import StringIO
import json
from urllib import urlencode


def send_turing(key, info, userid):
    c = pycurl.Curl()
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    result = StringIO.StringIO()
    data = urlencode({
        "key": key,
        "info": info.encode('utf-8'),
        "userid": userid

    })
    # TODO: use local cert to prevent from MITM, worst idea ever.
    url = 'https://www.tuling123.com/openapi/api'

    c.setopt(pycurl.CUSTOMREQUEST, 'POST')
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.WRITEFUNCTION, result.write)
    c.perform()
    c.close()
    return json.loads(result.getvalue()).get('text')


if __name__ == '__main__':
    pass
