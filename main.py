#!/usr/bin/python
# coding:utf-8


import telebot
# import logging
import kuaidi100
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
    bot.send_message(message.chat.id, '直接给我发送运单编号就好啦')


@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "呀你好\n我是一个能帮你查快递的机器人。有问题请联系 @BennyThink ")


@bot.message_handler(commands=['list'])
def bot_list(message):
    all_info = kuaidi100.list_query(message.chat.id)
    if all_info:
        for i in all_info:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, i[0] + ' ' + i[1] + '\n' + i[2] + i[3])
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '--o(*￣▽￣*)o--\n你还没有查询过呢~')


@bot.message_handler(commands=['delete'])
def bot_delete(message):
    if message.text == '/delete':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '把你的运单编号附加到delete之后，i.e. \n/delete 123456789')
    else:
        msg = kuaidi100.delete(message.text[8:])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['quickdel'])
def bot_quick_delete(message):
    if message.reply_to_message is None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '别调戏我了，讨厌鬼')
    else:
        s = message.reply_to_message.text
        msg = kuaidi100.delete(s.split()[0])
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, msg)


@bot.message_handler()
def track_express(message):
    if '.' in message.text:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '哎呀，你坏人，讨厌了啦')
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
