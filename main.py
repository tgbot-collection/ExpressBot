#!/usr/bin/python
# coding:utf-8


import telebot
import logging
import kuaidi100
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


# start - 输入快递单号来查询
# help - 帮助
# list - 查看我的查询历史
# delete - 删除某个单号

@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_message(message.chat.id, '直接给我发送单号就可以啦~')


@bot.message_handler(func=lambda message: True)
def track_express(message):
    # bot.send_message(message.chat.id, 'come again?')
    bot.send_chat_action(message.chat.id, 'typing')
    r = kuaidi100.recv(message.text, message.chat.username, message.chat.id)
    bot.send_message(message.chat.id, r)


bot.polling()
