#!/usr/bin/python
# coding:utf-8


import telebot
# import logging
import kuaidi100
import utils
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


# start - 输入快递单号来查询
# help - 帮助
# list - 查看我的查询历史记录
# delete - 删除某个单号查询记录
# quickdel - 回复某条查询消息来快速删除单号查询记录


@bot.message_handler(commands=['start'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '直接把运单号告诉咱就好啦 ~')


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "咱能帮汝查询快（shui）递（biao）信息啦~ 有问题的话就去 @BennyThink 呗。")


@bot.message_handler(commands=['list'])
def bot_list(message):
    all_info = kuaidi100.list_query(message.chat.id)
    if all_info:
        for i in all_info:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(
                message.chat.id, i[0] + ' ' + i[1] + '\n' + i[2] + i[3])
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
        bot.send_message(message.chat.id, utils.reply_fefuse())
    else:
        s = message.reply_to_message.text
        msg = kuaidi100.delete(s.split()[0])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler()
def track_express(message):
    if '.' in message.text:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, utils.reply_fefuse())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        r = kuaidi100.recv(message.text, message.message_id, message.chat.id)
        bot.send_message(message.chat.id, r)


# TODO: Improve echo msg
@bot.message_handler()
def cron(code, mid, cid, db_content):
    r = kuaidi100.recv(code, mid, cid)
    if db_content not in r:
        bot.send_message(chat_id=cid, reply_to_message_id=mid, text=db_content)


if __name__ == '__main__':
    bot.polling()
