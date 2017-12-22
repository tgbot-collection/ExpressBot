#!/bin/bash
# check status and restart it if necessary.

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export TOKEN=''
export DB_PATH='/home/ExpressBot/expressbot/bot.db'

python /home/ExpressBot/expressbot/timer.py