#!/bin/bash
# check bot status and reboot it if necessary.

ps -elf|grep 'python main.py'|grep -v grep
if [ $? -eq 0 ];then
  echo 'running'
else
  echo 'stop'
  screen -list|grep bot
  if [ $? -eq 1 ];then
    echo 'screen does not exists.'
    screen -S bot
    python /home/ExpressBot/main.py
  else
    echo 'restoring screen...'
    screen -r bot
    python /home/ExpressBot/main.py
  fi    
fi
