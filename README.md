ExpressBot [![Build Status](https://travis-ci.org/BennyThink/ExpressBot.svg?branch=master)](https://travis-ci.org/BennyThink/ExpressBot)
==

帮你查快递、自动追踪快递最新状态的Telegram机器人！
成品可戳

[@bennyblog_bot](https://t.me/bennyblog_bot)

[@xiaowu_bot](https://t.me/xiaowu_bot)

这个机器人不只是能聊天、查快递哦！详细信息可以看功能和TODO

## 功能 ##
* 查快递
* 列出历史查询
* 聊天
* 群组聊天（使用/开头、回复机器人消息来呼叫机器人）：由于开启了隐私模式，所以只好这样啦~
命令列表：

> start - 输入快递单号来查询 
>
> help - 帮助
>
> list - 查看我的查询历史记录
>
> delete - 删除某个单号查询记录
>
> quickdel - 回复某条查询消息来快速删除单号查询记录
 
## 部署环境 ##
需要部署在可以访问Telegram API的服务器上（或者设置代理），同时支持Python 2和Python 3
已经在以下平台测试通过：

Windows 10： Python 2.7.13 32bit  Python 3.6.3 32bit

Ubuntu 16.04、CentOS 7、Debian 9： Python 2.7

```
关于Centos：
BennyThink:反正我是测试通过了
johnpoint：反正我这边没有成功过
     ——————各位自便
```


## 部署方法1.自动脚本 ##

一键脚本只支持Python 2，已经在Ubuntu 16.04、CentOS 7、Debian 9的64位版本上测试通过：

```
wget -N --no-check-certificate https://raw.githubusercontent.com/BennyThink/ExpressBot/master/install.sh && chmod +x install.sh && ./install.sh
```
快捷操作
```
启动服务 ./install.sh start
停止服务 ./install.sh stop
```
注：CentOS下可能有些事多，比如偶然发现安装完epel之后竟然就有pycurl了；如果提示`wget: command not found`请先安装wget `yum install wget`

## 部署方法2.手动配置 ##
如果一键脚本失败，可以试试手动配置
### 克隆代码 ###
```
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
```
### 准备环境 ###
#### Arch Linux  ####
```
pacman -S python python-pip python-certifi python-chardet python-future python-idna python-pycurl python-requests python-six python-urllib3
```
    然后从 AUR 安装  python-pytelegrambotapi .

#### 其他发行版、macOS ####
Python3 请使用`pip3`
```
pip install -r requirements.txt
```
    如果pip时报错，那么就先运行下面这句（Debian系）
    sudo apt-get install libcurl4-openssl-dev
	
	RHEL系（跟你说，出错了别赖我哦）
	sudo yum install libcurl-devel

#### Windows  ####
从[Python官网](https://www.python.org/)下载并安装Python，切换到项目目录，如果是 Python 2:
```
pip install -r requirements.txt
```
如果是 Python 3,点击[此处下载](http://www.lfd.uci.edu/~gohlke/pythonlibs/zhckc95n/pycurl-7.43.0-cp36-cp36m-win32.whl)`pycurl`，执行如下命令：
```
pip3 install wheel
pip3 install pycurl-7.43.0-cp36-cp36m-win32.whl
pip3 install -r requirements.txt
```

### 配置 ###
修改`config.py`进行配置，TOKEN为Bot的API，TURING_KEY若不配置则不启用机器人功能，DEBUG为设置是否在控制台输出debug信息，0为不输出

```
TOKEN = 'Your TOKEN'
TURING_KEY = 'Your Key'
DEBUG = 0
```

### 运行 ###
测试目的的话，以nohub或screen运行`main.py`，Python 3请用`python3`替换为`python`
```
cd /your/path/ExpressBot/expressbot
nohup python main.py
# 或者
cd /your/path/ExpressBot/expressbot
screen -S tgbot
python main.py
```
将timer加入到任务计划中（Linux为crontab），如下
`*/2 * * * * cd /your/path/ExpressBot/expressbot && python main.py`
即为两分钟运行一次
**由于一些问题，计划任务目前只支持在Linux上使用，并且是程序目录为`/home/ExpressBot`才可以
查看TODO获取更多信息**

###  检查运行状态 ###
由于因为网络原因，有时程序会抛异常（requests的锅，这个没法控制），所以需要用某种办法守护它。

（**只适用于systemd**）编辑你自己的`expressbot.service`，然后将其复制到`/lib/systemd/system/expressbot.service`,并使用如下命令启动：
```
sudo systemctl daemon-reload
sudo systemctl enable expressbot.service
```
查看运行状态
```
sudo systemctl status expressbot.service
```
启动
```
sudo systemctl start expressbot.service
```
停止
```
sudo systemctl stop expressbot.service
```
然后把`bot_check.sh`加入到crontab中，比如说：
`
*/2 * * * * bash /home/ExpressBot/bot_check.sh
`
## 隐私 ##
首先，请允许我大力的打击你，所有发往此机器人的消息都可能被记录下来。
但是实际上，此机器人会在数据库中记录查询成功之后的以下信息，使用`/list`命令可以看到：
* message_id 每条消息的id，用于任务计划跟踪物流发送回复
* chat_id 也是用户ID，用于标记回复给谁
* type 快递公司名称
* track_id 运单编号
* content 最新的物流信息
* status 快递状态
* date 最新物流更新时间

我不保证我能够有节操不去查看数据库，但是我保证我会妥善保护数据库、不外泄。

所以，你要是不想用，就不用吧；或者，查完就删掉也是可以的。

## FAQ ##
### 服务器错误 ###
唔，可能是快递100的接口炸了吧；稍后重试吧。
### SSL InsecurePlatform error ###
哦，你可能用的是 Python 3.5 吧，建议还是用回 Python 2.7吧，要不Python 3.6也行吧。

## 致谢 ##
* [coderfox/Kuaidi100API](https://github.com/coderfox/Kuaidi100API)
* [jaehee~임재희](https://twitter.com/GFW) 感谢你的大力调戏
* [ヨイツの賢狼ホロ](https://github.com/KenOokamiHoro) 感谢你的commits，我直接无耻的拉过来了。
* [johnpoint](https://github.com/johnpoint) 一键安装脚本的大部分编写工作

## TODO ##
- [x] 这个机器人可以跟你聊天扯淡呢~
- [x] Python 3 支持
- [x] Bug 修复：不显示最新
- [ ] SSL 证书问题
- [ ] 下载YouTube视频
- [ ] 下载Google Play应用
- [ ] 添加测试用例
- [ ] Google搜索

## bug fix ##
* `db.py`中数据库路径的处理方式，在执行计划任务的时候，会导致使用根目录下的`bot.db`，所以目前暂时使用绝对路径；
还有，如果用户查询了追踪中的快递，然后block了机器人，这将会导致机器人发送消息时抛出异常：
```telebot.apihelper.ApiException: A request to the Telegram API was unsuccessful. The server returned HTTP 403 Forbidden. Response body:
[{"ok":false,"error_code":403,"description":"Forbidden: bot was blocked by the user"}]
```
捕获一下就可以了。
比较好的解决方式：在配置文件中指定数据库（项目）路径

## License ##
GPL v2
