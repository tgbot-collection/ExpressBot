#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#=================================================
#	System Requirements:
#   Debian 6+, Ubuntu 14.04+, CentOS 7+,
#   better with systemd.
#	Version: 4.3.1
#	Blog: blog.lvcshu.club
#	Author: johnpoint
#   Maintain: BennyThink
#   Install Express Bot
#   Requires root privilege
#   This code is tested under Ubuntu 16.04, CentOS 7 and Debian 9.
#   Publish under GNU General Public License v2
#   USE AT YOUR OWN RISK!!!
#=================================================

sh_ver="4.3.1"
Green_font_prefix="\033[32m" && Red_font_prefix="\033[31m" && Green_background_prefix="\033[42;37m" && Red_background_prefix="\033[41;37m" && Font_color_suffix="\033[0m"
Info="${Green_font_prefix}[信息]${Font_color_suffix}"
Error="${Red_font_prefix}[错误]${Font_color_suffix}"
Tip="${Green_font_prefix}[注意]${Font_color_suffix}"
Separator_1="——————————————————————————————"

Get_Dist_Name()
{
    if grep -Eqi "CentOS" /etc/issue || grep -Eq "CentOS" /etc/*-release; then
        DISTRO='CentOS'
        PM='yum'
    elif grep -Eqi "Red Hat Enterprise Linux Server" /etc/issue || grep -Eq "Red Hat Enterprise Linux Server" /etc/*-release; then
        DISTRO='RHEL'
        PM='yum'
    elif grep -Eqi "Aliyun" /etc/issue || grep -Eq "Aliyun" /etc/*-release; then
        DISTRO='Aliyun'
        PM='yum'
    elif grep -Eqi "Fedora" /etc/issue || grep -Eq "Fedora" /etc/*-release; then
        DISTRO='Fedora'
        PM='yum'
    elif grep -Eqi "Amazon Linux AMI" /etc/issue || grep -Eq "Amazon Linux AMI" /etc/*-release; then
        DISTRO='Amazon'
        PM='yum'
    elif grep -Eqi "Debian" /etc/issue || grep -Eq "Debian" /etc/*-release; then
        DISTRO='Debian'
        PM='apt'
    elif grep -Eqi "Ubuntu" /etc/issue || grep -Eq "Ubuntu" /etc/*-release; then
        DISTRO='Ubuntu'
        PM='apt'
    elif grep -Eqi "Raspbian" /etc/issue || grep -Eq "Raspbian" /etc/*-release; then
        DISTRO='Raspbian'
        PM='apt'
    elif grep -Eqi "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
        PM='apt'
    else
        DISTRO='unknow'
    fi

}


 
# Install_all
Install_all(){
if [ "$PM" = "yum" ]; then
	$PM install -y epel-release
	$PM update
    $PM install -y python-pip git
    Install_main
    install_service
    Start_service
elif [ "$PM" = "apt" ]; then
	$PM update
    $PM install -y build-essential curl python-dev python-pip libssl-dev git libcurl4-openssl-dev
    pip install  setuptools
    Install_main
    install_service
    Start_service
fi
}


 
# Install_main
Install_main(){
cd /home
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
if [ "$PM" = "yum" ]; then
    echo 'centosssssssssss:-)'
    sed -i '$d' requirements.txt
fi
pip install -r requirements.txt

echo 'Input your Token (telegram bot)'
read p
echo "TOKEN = '$p'">/home/ExpressBot/expressbot/config.py

echo 'Input your Turing Key, blank/space to disable'
read p
echo "TURING_KEY ='$p'">>/home/ExpressBot/expressbot/config.py

echo 'Debug? 0 for no.'
read p
echo "DEBUG= '$p'">>/home/ExpressBot/expressbot/config.py

echo "* * * * * /home/ExpressBot/bot_checker.sh" >> /var/spool/cron/root

}

check_systemd(){
systemctl --version>>/dev/null
if [ $? -ne 0 ];then
    echo -e "${Tip} 非systemd"
    exit 0
fi
}

install_service(){
check_systemd
cp expressbot.service /lib/systemd/system/expressbot.service
systemctl daemon-reload
systemctl enable expressbot.service
}

remove_service(){
sed -i '$d' /var/spool/cron/root
check_systemd
systemctl stop expressbot.service
systemctl disable expressbot.service
rm /lib/systemd/system/expressbot.service
systemctl daemon-reload
}

# Start_service
Start_service(){
check_systemd
systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo -e "${Info}服务已经启动"
  exit 0
else
  echo -e "${Info}服务正在启动"
  systemctl start expressbot.service
fi
systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo -e "${Info}服务启动成功"
  exit 0
else
  echo -e "${Error}服务启动失败"
fi
}

# Stop_service
Stop_service(){
check_systemd
systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo -e "${Info}正在停止服务"
  systemctl stop expressbot.service
else
  echo -e "${Error}服务已经停止"
fi
systemctl status expressbot.service>/dev/null
if [ $? -eq 0 ];then
  echo -e "${Error}服务停止失败"
else
  echo -e "${Info}服务已停止"
fi
}
uninstall_all(){
pip uninstall -y -r /home/ExpressBot/requirements.txt
rm -rf /home/ExpressBot
# It's better not to remove packages.
#if [ "$PM" = "yum" ]; then
#    $PM remove -y libcurl-devel openssl-devel
#elif [ "$PM" = "apt" ]; then
#    $PM remove -y libssl-dev libcurl4-openssl-dev
#fi
remove_service
}

# Restart_service
Restart_service(){
check_systemd
Stop_service
Start_service
}

# Service_status
Service_status(){
check_systemd
systemctl status expressbot.service
}

menu(){
	echo -e "  Express Bot一键管理脚本 ${Red_font_prefix}[v${sh_ver}]${Font_color_suffix}
  ---- 主程序：BennyThink  | 脚本：johnpoint ----
  ——————————————————————
  ${Green_font_prefix}1.${Font_color_suffix} 一键 安装
  ——————————————————————
  ${Green_font_prefix}2.${Font_color_suffix} 一键 卸载
  ——————————————————————
  ${Green_font_prefix}3.${Font_color_suffix} 启动 服务
  ${Green_font_prefix}4.${Font_color_suffix} 停止 服务
  ${Green_font_prefix}5.${Font_color_suffix} 重启 服务
  ${Green_font_prefix}6.${Font_color_suffix} 查看 服务状态
  ——————————————————————
 "
	read -p "请输入数字 [1-6]：" num
case "$num" in
	1)
	Install_all
	;;
	2)
	uninstall_all
	;;
	3)
	Start_service
	;;
	4)
	Stop_service
	;;
	5)
	Restart_service
	;;
	6)
	Service_status
	;;
	*)
	echo -e "${Error} 请输入正确的数字 [1-6]"
	;;
esac
}


# main goes here...
Get_Dist_Name

# check distribution
if [ "${DISTRO}" = "unknow" ]; then
    Echo -e "${Error} 无法获取发行版名称，或者不支持当前发行版"
    exit 1
fi

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
