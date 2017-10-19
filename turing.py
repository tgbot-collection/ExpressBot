#!/usr/bin/python
# coding:utf-8

# Turing robot, requires TURING_KEY in config.py
__author__ = 'Benny <benny@bennythink.com>'

import pycurl
import json

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def send_turing(key, info, userid):
    """
    send request to Turing robot, and get a response
    :param key: TURING_KEY
    :param info: the message from user
    :param userid: chat_id, for context parse
    :return: response from Turing Bot, in text.
    """
    try:
        info = info.encode('utf-8')
    except UnicodeDecodeError:
        pass

    try:
        import StringIO
        result = StringIO.StringIO()
    except ImportError:
        import io
        result = io.BytesIO()

    c = pycurl.Curl()
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    data = urlencode({
        "key": key,
        "info": info,
        "userid": userid

    })

    # TODO: use local cert to prevent from MITM, worst idea ever.
    url = 'https://www.tuling123.com/openapi/api'

    c.setopt(pycurl.CUSTOMREQUEST, 'POST')
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.WRITEFUNCTION, result.write)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.perform()
    c.close()
    return json.loads(result.getvalue()).get('text')


if __name__ == '__main__':
    pass
