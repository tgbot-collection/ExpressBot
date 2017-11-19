#!/bin/bash
# check bot status and restart it if necessary.
# Requires root privilege

systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo 'running'
else
  echo 'stop'
  systemctl start expressbot.service
fi
