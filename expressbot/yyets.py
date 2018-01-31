#!/usr/bin/python
# coding:utf-8

# ExpressBot - yyets.py
# 2018/1/3 11:01
# YYeTs API
# Python 2 & 3

__author__ = 'Benny <benny@bennythink.com>'

import requests


def show_resource(resource_id):
    """
    show resource information.
    :param resource_id: unique id for each resource, get from `search_resource`
    :return: download link in json
    """
    url = 'http://pc.zmzapi.com/index.php?g=api/pv2&m=index&a=resource&accesskey=519f9cab85c8059d17544947k361a827&id='
    r = requests.get(url + resource_id)
    return r.json()


def search_resource(name):
    """
    search resource
    :param name: tv/movie name
    :return: the whole search result
    """
    url = 'http://pc.zmzapi.com/index.php?g=api/pv2&m=index&a=search&accesskey=519f9cab85c8059d17544947k361a827&limit=200&k='
    r = requests.get(url + name)
    return r.json()


def query_resource(user_raw_message):
    """
    query resource name
    :param user_raw_message: `/query batman`
    :return: message to be sent/
    """
    name = user_raw_message[6:].lstrip(' ').rstrip(' ')

    search_result = search_resource(name)
    msg = ''
    s = search_result.get('data')
    if s is None:
        return '没有对应的资源，使用方法/query 逃避可耻却有用'
    elif len(s) > 1:
        for key in range(len(s)):
            msg = msg + ('%d. %s %s' % (key + 1, s[key].get('channel'), s[key].get('title'))) + '\n'
    return msg


def get_season_count(tv_name):
    """
    if it was movie, get download link whenever possible; if it was tv, get seasons count
    :param tv_name: name, such as `avatar`, `Black Mirror`
    :return: download link, `0, err_msg` or `season count, dl link`
    """
    search_result = search_resource(tv_name)

    if search_result.get('data') is None:
        return 0, '没有这个资源'
    elif len(search_result.get('data')) > 1:
        return 0, '关键词不够精确哦，不如试试/query 关键词吧！'
    elif search_result.get('data')[0].get('channel') == 'movie':
        # TODO: AccessKey  4002 资源关闭 4003暂时没有资源
        download_link = show_resource(search_result.get('data')[0].get('id'))
        if download_link.get('status') != 1:
            return 0, '由于accesskey的原因，电影搜索基本是废的，正在尝试修复中……'
        else:
            return 255, get_movie_link(download_link)
    else:
        download_link = show_resource(search_result.get('data')[0].get('id'))
        if download_link.get('status') != 1:
            return 0, '资源不可用'

        season = download_link.get('data').get('list')[0].get('season')
        if season == '101':
            return 1, download_link
        else:
            return int(season), download_link


def get_movie_link(data):
    """
    get movie link
    :param data: link generate by `show_resource`
    :return: pass two params to iter_link to get actual link
    """
    dl_list = data.get('data').get('list')[0].get('episodes')[0]

    dl_hr_mp4 = dl_list.get('files').get('HR-HDTV') or dl_list.get('files').get('MP4')
    dl_app = dl_list.get('files').get('APP')
    return iter_link(dl_app, dl_hr_mp4)


def get_episode_count(data):
    """
    get episode count, show it in InlineKeyBoard
    :param data: 神盾局 3
    :return: episode count
    """

    _, dl = get_season_count(data.split(' ')[0])
    n = int(data.split(' ')[1])
    length = len(dl.get('data').get('list'))
    return len(dl.get('data').get('list')[length - 1 - n].get('episodes')), dl.get('data').get('list')[
        length - 1 - n].get('episodes')


def get_tv_link(data):
    """
    get tv link for specified seasons and episodes.
    :param data: 神盾局 4 16
    :return: pass two params to iter_link to get actual link
    """
    name = data.split(' ')[0]
    season = data.split(' ')[1]
    ep = int(data.split(' ')[2])
    ep_count, dl_list = get_episode_count(name + ' ' + season)

    # HR-HDTV/MP4 or APP
    dl_hr_mp4 = dl_list[ep_count - ep].get('files').get('HR-HDTV') or dl_list[ep_count - ep].get('files').get('MP4')
    dl_app = dl_list[ep_count - ep].get('files').get('APP')
    return iter_link(dl_app, dl_hr_mp4)


def iter_link(dl_app, dl_hr_mp4):
    """
    iterate links from dict
    :param dl_app: app link dict
    :param dl_hr_mp4: HR-HDTV/MP4 link dict
    :return: possible download link, str
    """
    dl_add = ''
    for key in dl_app:
        if key.get('way') == '102':
            dl_add = dl_add + u'微云：' + key.get('address') + '\n\n'
        elif key.get('way') == '103':
            dl_add = dl_add + u'A站：' + key.get('address') + '\n\n'
        elif key.get('way') == '104':
            dl_add = dl_add + u'B站：' + key.get('address') + '\n\n'
        elif key.get('way') == '114':
            dl_add = dl_add + u'范特西：' + key.get('address') + '\n\n'
        elif key.get('way') == '115':
            dl_add = dl_add + u'微云：' + key.get('address') + '\n\n'

    for key in dl_hr_mp4:
        if key.get('way') == '1':
            dl_add = dl_add + u'电驴ed2k：' + key.get('address') + '\n\n'
        elif key.get('way') == '2':
            dl_add = dl_add + u'磁力链：' + key.get('address') + '\n\n'
        elif key.get('way') == '9':
            dl_add = dl_add + u'网盘：' + key.get('address') + '\n\n'
        elif key.get('way') == '12':
            dl_add = dl_add + u'城通网盘：' + key.get('address') + '\n\n'

    return dl_add


if __name__ == '__main__':
    print(get_season_count('神盾局'))
