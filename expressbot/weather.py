#!/usr/bin/python
# coding:utf-8

# ExpressBot - weather.py
# 2018/4/6 19:53
# weather broadcast for 7 days

__author__ = 'Benny <benny@bennythink.com>'

import requests

from constants import CITY

URL = u'http://wthrcdn.etouch.cn/weather_mini?citykey='


def forecast_5d(city, length):
    """
    get the next 5 day's weather forecast
    :param length: breaker length
    :param city: city name in unicode
    :return: forecast in string.
    """
    city_code = CITY.get(city)
    if city_code is None:
        return '啊哦，没有查询到你要的信息'
    r = requests.get(URL + city_code).json()

    if r['status'] != 1000:
        return '啊哦，没有查询到你要的信息'

    msg = u'%s 天气预报\n%s\n空气质量指数：%s\n%s\n%s%s\n%s'
    five_day = ''
    yesterday = r["data"]["yesterday"]['date'] + '    ' + r["data"]["yesterday"]['type'] + '    ' + \
                r["data"]["yesterday"]['high'] + ' ' + r["data"]["yesterday"]['low'] + '    ' + \
                r["data"]["yesterday"]['fx'] + r["data"]["yesterday"]['fl'].split('[')[2].split(']')[0]

    for i in r["data"]["forecast"]:
        five_day = five_day + i['date'] + '    ' + i['type'] + '    ' + i['high'] + ' ' + i['low'] + '    ' + \
                   i['fengxiang'] + i['fengli'].split('[')[2].split(']')[0] + '\n'

    return msg % (r['data']['city'], yesterday, r['data']['aqi'], '-' * length, five_day, '-' * length,
                  r['data']['ganmao'])


if __name__ == '__main__':
    print(forecast_5d(u'重庆', 30))
