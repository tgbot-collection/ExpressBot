#!/usr/bin/python
# coding:utf-8

# Telegram message handle function.
__author__ = 'Benny <benny@bennythink.com>'
__credits__ = 'ヨイツの賢狼ホロ <horo@yoitsu.moe>'
__version__ = '1.1.1'

import telebot
import kuaidi100
import turing
import utils
import os
import config
from msg import msg_logger
import speech
import requests
import db
import time

TOKEN = os.environ.get('TOKEN') or config.TOKEN
TURING_KEY = os.environ.get('TURING_KEY') or config.TURING_KEY
DEBUG = os.environ.get('DEBUG') or config.DEBUG

bot = telebot.TeleBot(TOKEN)


# TODO: Do I need to refactor `send_chat_action`?
@bot.message_handler(commands=['start'])
def bot_help(message):
    if message.text == '/start':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '直接把运单号告诉咱就好啦 ~')
    elif ',' in message.text:
        msg = message.text.split()[1].split(',')
        for item_tid in msg:
            bot.send_chat_action(message.chat.id, 'typing')
            r = kuaidi100.recv(item_tid, message.message_id, message.chat.id)
            bot.send_message(message.chat.id, r)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        r = kuaidi100.recv(message.text.split()[1], message.message_id, message.chat.id)
        bot.send_message(message.chat.id, r)


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "咱能帮汝查询快（shuǐ）递（biǎo）信息啦~ 有问题的话就去 @BennyThink 呗。")
    bot.send_message(message.chat.id,
                     "直接发送运单编号即可查询（并添加到追踪中）；\
                     如果汝的单号带有字母，请使用/start danhao123；\
                     如果汝需要一次性追踪多个单号，请/start 123,1234，使用英文半角逗号分隔。")


@bot.message_handler(commands=['list'])
def bot_list(message):
    all_info = kuaidi100.list_query(message.chat.id)
    if all_info:
        for i in all_info:
            bot.send_chat_action(message.chat.id, 'typing')

            # print type(i[2])

            bot.send_message(
                message.chat.id, i[0] + '  ' + i[1] + '\n' + i[2] + i[3])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '--o(*￣▽￣*)o--\n诶汝有问过咱嘛？')


@bot.message_handler(commands=['delete'])
def bot_delete(message):
    if message.text == '/delete':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(
            message.chat.id, '/delete 123456789\n像这样把汝的运单编号加到 /delete 之后就好啦~/')
    else:
        msg = kuaidi100.delete(message.text[8:])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['quickdel'])
def bot_quick_delete(message):
    if message.reply_to_message is None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, utils.reply_refuse())
    else:
        s = message.reply_to_message.text
        msg = kuaidi100.delete(s.split()[0])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text', 'voice'])
@msg_logger
def track_express(message):
    """
    process text/voice message, all digits means express id. Otherwise sends Turing or refuse message
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
        file_path = temp + os.sep
        with open(file_path + message.voice.file_id + '.ogg', 'wb') as f:
            f.write(voice_file.content)
        message.text = speech.voice_to_text(file_path, message.voice.file_id + '.ogg')

    if u'4C7' in message.text:
        bot.send_chat_action(message.chat.id, 'typing')
        r = utils.reply_refuse()
        bot.send_message(message.chat.id, r)
        return r
    elif message.text.isdigit():
        bot.send_chat_action(message.chat.id, 'typing')
        r = kuaidi100.recv(message.text, message.message_id, message.chat.id)

        if u'单号不存在或者已经过期' in r:
            bot.send_message(message.chat.id, '汝的单号可能刚刚生成，暂无信息，已经加入到任务队列中')
            sql_cmd = "INSERT INTO job VALUES (NULL ,?,?,?,? ,'刚刚录入耶' ,'Started',?,0)"

            db.upsert(sql_cmd,
                      (message.message_id, message.chat.id,
                       kuaidi100.auto_detect(message.text)[0], message.text,
                       time.strftime("%Y-%m-%d %H:%M:%S")))
        else:
            bot.send_message(message.chat.id, r)
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
    if DEBUG == '1':
        import logging

        logger = telebot.logger
        telebot.logger.setLevel(logging.DEBUG)

    bot.polling(none_stop=True)
