#!/usr/bin/python
# coding:utf-8

# configuration
import os

# Mandatory
TOKEN = 'TOKEN'
# Optional, if you leave TURING_KEY with blank, the robot won't chat with you.
TURING_KEY = 'KEY'

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bot.db')
# minutes
INTERVAL = 120

LOGGER = False
