#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#=================================================
#	System Required: Debian 6+/Ubuntu 14.04+
#	Version: 3.2.0
#	Blog: blog.lvcshu.club
#	Author: johnpoint
#   Install Express Bot
#   Requires root privilege
#   This code is not tested, use at your own risk!!
#   警告！请勿用于生产环境！！！
#=================================================

sh_ver="3.2.0"
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

 #check_sys
 check_sys(){
 if [[ ${OS} == 'CentOS' ]];then 
 echo "${Error} 抱歉，本脚本不支持此系统"
 exit 1
 else 
 echo -e "${Info} 开始执行脚本"
 fi
 }
 
 #Install_all
 Install_all(){
 Install_something
 Install_main
 Start_service
 }
 
 #Install_something
 Install_something(){
apt update
apt upgrade
apt-get install python-dev systemd python-pip libssl-dev libxtst-dev git libghc-gnutls-dev libcurl4-openssl-dev
apt-get build-dep python-lxml
pip install lxml --upgrade
pip install --upgrade pip
pip install pycurl
 }
 
 #Install_main
 Install_main(){
cd /home
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
pip install -r requirements.txt

echo 'Input your Token (telegram bot)'
read p
echo "TOKEN = '$p'">config.py

echo 'Input your Turing Key, blank/space to disable'
read p
echo "TURING_KEY ='$p'">>config.py

echo 'Debug? 0 for no.'
read p
echo "DEBUG= '$p'">>config.py

echo "*/2 * * * * /home/ExpressBot/bot_checker.sh" >> /var/spool/cron/root
cp expressbot.service /lib/systemd/system/expressbot.service
systemctl daemon-reload
systemctl enable expressbot.service
Start_service
 }

 #Start_service
 Start_service(){
systemctl start expressbot.service
echo -e "${Info}服务已启动"
}

#Stop_service
Stop_service(){
systemctl stop expressbot.service
echo -e "${Info}服务已停止"
}
#Restart_service
Restart_service(){
Stop_service
Start_service
}
#Service_status
Service_status(){
systemctl status expressbot.service
}

menu(){
	echo -e "  Express Bot一键管理脚本 ${Red_font_prefix}[v${sh_ver}]${Font_color_suffix}
  ---- 主程序：BennyThink  | 脚本：johnpoint ----
  ——————————————————————
  ${Green_font_prefix}1.${Font_color_suffix} 一键 安装
  ——————————————————————
  ${Green_font_prefix}2.${Font_color_suffix} 安装 依赖
  ${Green_font_prefix}3.${Font_color_suffix} 安装 主程序
  ——————————————————————
  ${Green_font_prefix}4.${Font_color_suffix} 启动 服务
  ${Green_font_prefix}5.${Font_color_suffix} 停止 服务
  ${Green_font_prefix}6.${Font_color_suffix} 重启 服务
  ${Green_font_prefix}7.${Font_color_suffix} 查看 服务状态
  ——————————————————————
 "
	echo && stty erase '^H' && read -p "请输入数字 [1-15]：" num
case "$num" in
	1)
	Install_all
	;;
	2)
	Install_something
	;;
	3)
	Install_main
	;;
	4)
	Start_service
	;;
	5)
	Stop_service
	;;
	6)
	Restart_service
	;;
	7)
	Service_status
	;;
	*)
	echo -e "${Error} 请输入正确的数字 [1-7]"
	;;
esac
}
check_sys
action=$1
if [[ ! -z $action ]]; then
	if [[ $action = "start" ]]; then
		Start_service
	elif [[ $action = "stop" ]]; then
		Stop_service
	fi
else
	menu
fi
