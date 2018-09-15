#!/usr/bin/python
# coding:utf-8

# Telegram message handle function.
__author__ = 'Benny <benny@bennythink.com>'
__credits__ = 'ヨイツの賢狼ホロ <horo@yoitsu.moe>'

import os
import time
import requests

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

import config
import kuaidi100
import turing
import yyets
import utils
from __init__ import __author__, __version__, __credits__, __website__, BANNER
from utils import msg_logger
from timer import checker
from weather import forecast_5d

TOKEN = os.environ.get('TOKEN') or config.TOKEN
TURING_KEY = os.environ.get('TURING') or config.TURING_KEY

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def bot_start(message):
    if message.text == '/start':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '哎哟欢迎😗我能查快递，陪聊，查美剧电影 ~\n要不戳这里试试看 /help')
    elif ',' in message.text:
        msg = message.text.split()[1].split(',')
        for item_tid in msg:
            bot.send_chat_action(message.chat.id, 'typing')
            r = kuaidi100.receiver(item_tid, message.message_id, message.chat.id)
            bot.reply_to(message, r, parse_mode='Markdown')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        r = kuaidi100.receiver(message.text.split()[1], message.message_id, message.chat.id)
        bot.reply_to(message, r, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "咱能帮汝查询快（shuǐ）递（biǎo）信息啦~ 有问题的话就去 @BennyThink 呗。\n"
                     "**⚠由于快递100的接口限制，可能会导致超出查询上限，目前已暂停轮询推送⚠**\n"
                     "项目地址 https://github.com/BennyThink/ExpressBot 欢迎PR", parse_mode='Markdown')
    bot.send_message(message.chat.id,
                     "直接发送运单编号即可查询（并添加到追踪中）\n"
                     "如果汝的单号带有字母，请使用`/start danhao123`\n"
                     "如果汝需要一次性追踪多个单号，请`/start 123,1234`，使用英文半角逗号分隔。",
                     parse_mode='Markdown')

    bot.send_message(message.chat.id,
                     "查询美剧/日剧/电影：`/query 蝙蝠侠`\n"
                     "查询美剧下载链接：`/yyets 神盾局`，之后按照提示点击按钮\n", parse_mode='Markdown')


@bot.message_handler(commands=['list'])
def bot_list(message):
    all_info = kuaidi100.list_query(message.chat.id)
    if all_info:
        for i in all_info:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(
                message.chat.id,
                '%s %s %s\n %s' % (i[4], i[3], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i[6]))), i[5]))
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '--o(*￣▽￣*)o--\n诶汝有问过咱嘛？')


@bot.message_handler(commands=['delete'])
def bot_delete(message):
    if message.text == '/delete':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(
            message.chat.id, '`/delete 123456789`\n像这样把汝的运单编号加到 `/delete` 之后就好啦~/', parse_mode='Markdown')
    else:
        r = kuaidi100.delete_record(message.text[8:])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, r)


@bot.message_handler(commands=['quickdel'])
def bot_quick_delete(message):
    if message.reply_to_message is None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, utils.reply_refuse())
    else:
        s = message.reply_to_message.text
        kuaidi100.delete_record(s.split()[0])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '删除成功')


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    previous = call.data
    btn_list = []
    size = 3
    markup = types.InlineKeyboardMarkup(size)

    if len(call.data.split(' ')) == 2:
        episode_count, _ = yyets.get_episode_count(call.data)

        for button in range(1, episode_count + 1):
            btn_list.append(types.InlineKeyboardButton("第%s集" % button, callback_data='%s %s' % (previous, button)))
        for i in range(0, len(btn_list), size):
            part = btn_list[i:i + size]
            if len(part) == 3:
                markup.add(part[0], part[1], part[2])
            elif len(part) == 2:
                markup.add(part[0], part[1])
            else:
                markup.add(part[0])

        bot.edit_message_text('那么看第几集好呢😘', chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

    else:
        bot.answer_callback_query(call.id, '汝要的信息取回来惹')
        bot.send_message(call.message.chat.id, yyets.get_tv_link(call.data))


@bot.message_handler(commands=['yyets'])
def bot_yyets(message):
    markup = types.InlineKeyboardMarkup()
    if message.text.count(' ') != 1:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '输入格式有误，例：`/yyets 神盾局特工`', parse_mode='Markdown')
        return
    bot.send_chat_action(message.chat.id, 'typing')
    season_count, msg = yyets.get_season_count(message.text.split(' ')[1])
    if season_count == 0:
        bot.send_message(message.chat.id, msg)
        return
    elif season_count == 255:
        bot.send_message(message.chat.id, msg)
        return
    for button in range(1, season_count + 1):
        markup.add(types.InlineKeyboardButton
                   ("第%s季" % button,
                    callback_data='%s %s' % (message.text.split(' ')[1], button)))
    bot.send_message(message.chat.id, "你想看第几季呢？请点击选择", reply_markup=markup)


@bot.message_handler(commands=['query'])
def bot_query(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg = yyets.query_resource(message.text)
    if msg == '':
        bot.send_message(message.chat.id, '好像出了点错误，使用方法`/query 逃避可耻却有用`', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['weather'])
def bot_weather(message):
    if len(message.text) == 8:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '使用方法：/weather 北京')
    else:
        bot.send_chat_action(message.chat.id, 'upload_document')
        msg = forecast_5d(message.text.split()[1], 30)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text', 'voice'])
@msg_logger
def track_express(message):
    """
    get_season_count text/voice message, all digits means express id. Otherwise sends Turing or refuse message
    :param message: Telegram message sent by user.
    :return: None
    """
    if os.name == 'nt':
        temp = os.environ.get('TMP')
    else:
        temp = '/tmp'

    if message.voice:
        bot.send_chat_action(message.chat.id, 'record_audio')
        # download the file
        file_info = bot.get_file(message.voice.file_id)
        voice_file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        file_path = os.path.join(temp, message.voice.file_id + '.ogg')
        with open(file_path, 'wb') as f:
            f.write(voice_file.content)
        message.text = utils.voice_to_text(file_path)

    if u'4C7' in message.text:
        bot.send_chat_action(message.chat.id, 'typing')
        r = utils.reply_refuse()
        bot.send_message(message.chat.id, r)
    elif message.text.isdigit():
        bot.send_chat_action(message.chat.id, 'typing')
        r = kuaidi100.receiver(message.text, message.message_id, message.chat.id)
        if u'单号不存在或者已经过期' in r:
            bot.reply_to(message, '汝的单号可能刚刚生成，暂无信息，不如稍后试试？')
        else:
            bot.reply_to(message, r, parse_mode='Markdown')
    # use turing bot
    elif TURING_KEY == '':
        bot.send_chat_action(message.chat.id, 'typing')
        r = utils.reply_refuse()
        bot.send_message(message.chat.id, r)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        r = turing.send_turing(TURING_KEY, message.text, message.chat.id)
        bot.send_message(message.chat.id, r)

    return r


if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(checker, 'interval', minutes=config.INTERVAL)
    scheduler.start()
    print('''Welcome to ExpressBot, Version %s\n%sAuthor: %s\nCredits:%s\nWebsite:%s\n%s'''
          % (__version__, BANNER, __author__, __credits__, __website__, '--' * 10 + 'Bot is running' + '--' * 10))
    bot.polling(none_stop=True)
