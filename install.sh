#!/bin/bash
# Install Express Bot
# Requires root privilege
# This code is not tested, use at your own risk!!

cd /home
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
apt update
apt-get install libcurl4-openssl-dev screen
pip install -r requirements.txt

echo 'Input your Token'
read p
echo "TOKEN = '$p'">config.py

echo 'Input your Turing Key, blank/space to disable'
read p
echo "TURING_KEY ='$p'">>config.py

echo 'Debug? 0 for no.'
read p
echo "DEBUG= '$p'">>config.py

echo "*/2 * * * * /home/ExpressBot/bot_checker.sh" >> /var/spool/cron/root

# starting bot
screen -S bot
python /home/ExpressBot/main.py