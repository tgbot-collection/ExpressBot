#!/bin/bash
# check bot status and restart it if necessary.
# Requires root privilege
# This script is obsolete, use systemd `Restart` instead.
systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo 'running' >/dev/null
else
  echo 'stop' >/dev/null
  systemctl start expressbot.service &>/dev/null
fi
