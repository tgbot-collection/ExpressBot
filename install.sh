#!/bin/bash
# Install Express Bot
# Requires root privilege
# This code is not tested, use at your own risk!!
# 警告！请勿用于生产环境！！！


Green_font_prefix="\033[32m" && Red_font_prefix="\033[31m" && Green_background_prefix="\033[42;37m" && Red_background_prefix="\033[41;37m" && Font_color_suffix="\033[0m"
Info="${Green_font_prefix}[信息]${Font_color_suffix}"
Error="${Red_font_prefix}[错误]${Font_color_suffix}"
Tip="${Green_font_prefix}[注意]${Font_color_suffix}"
Separator_1="——————————————————————————————"

#check OS#
if [ -f /etc/redhat-release ];then
 OS='CentOS'
 elif [ ! -z "`cat /etc/issue | grep bian`" ];then
 OS='Debian'
 elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
 OS='Ubuntu'
 else
 echo "Not support OS, Please reinstall OS and retry!"
 exit 1
 fi

 if [[ ${OS} == 'CentOS' ]];then 
 echo '${Error} 抱歉，本脚本不支持此系统'
 exit 1
 else 
 echo '${Info} 开始安装...'
 fi
apt update
apt upgrade
apt-get install python-dev systemd python-pip libssl-dev libxtst-dev git libghc-gnutls-dev libcurl4-openssl-dev
apt-get build-dep python-lxml
pip install lxml --upgrade
pip install --upgrade pip
pip install pycurl
cd /home
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
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
cp expressbot.service /lib/systemd/system/expressbot.service
systemctl daemon-reload
systemctl enable expressbot.service
systemctl start expressbot.service