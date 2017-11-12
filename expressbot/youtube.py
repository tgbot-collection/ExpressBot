#!/usr/bin/python
# coding:utf-8

# ExpressBot - youtube.py
# 2017/10/21 15:20
#
from __future__ import unicode_literals

__author__ = 'Benny <benny@bennythink.com>'

import youtube_dl
from expressbot import utils
import os


def dl(url_list):
    dl = youtube_dl.YoutubeDL()
    os.chdir('ydl')
    try:
        s = str(url_list)
        s = s[s.index('http'):]
        l = [s]
        dl.download(l)
        os.chdir('../')
        # TODO：How to deal with Chinese file name?
        return [i for i in os.listdir('./') if 'py' not in i][0]

    except youtube_dl.DownloadError as e:
        return utils.reply_not_found(), e.message


if __name__ == '__main__':
    pass
