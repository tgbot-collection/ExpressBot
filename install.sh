#!/bin/bash
# Install Express Bot
# Requires root privilege
# This code is not tested, use at your own risk!!


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
 echo '抱歉，本脚本不支持此系统'
 exit 1
 else 
 echo '开始安装...'
 fi
 
 
 cd /home
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
apt update
apt-get install libcurl4-openssl-dev systemd -y
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
systemctl start autorun.service