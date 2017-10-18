ExpressBot
==

帮你查快递、自动追踪快递最新状态的Telegram机器人！
成品可戳[https://t.me/bennyblog_bot](https://t.me/bennyblog_bot)

## 部署方法 ##
需要部署在可以访问Telegram API的服务器上（或者设置代理）
### 准备环境 ###
```
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
```

Arch Linux :
```
pacman -S python python-pip python-certifi python-chardet python-future python-idna python-pycurl python-requests python-six python-urllib3
```
    然后从 AUR 安装  python-pytelegrambotapi .

其他系统：
```
pip install -r requirements.txt
```
    如果pip时报错，那么就先运行下面这句（Debian系）
    
    sudo apt-get install libcurl4-openssl-dev
	
	RHEL系
	sudo yum install libcurl-devel

### 配置 ###
修改`config.py`中的TOKEN，TURING_KEY若不配置则不启用机器人功能。

```
TOKEN = 'YourToken'
```

### 运行 ###

以nohub或screen运行`main.py`
```
cd /your/path/ExpressBot
nohup python main.py
# 或者
cd /your/path/ExpressBot/
screen -S tgbot
python main.py
```
将timer加入到任务计划中（Linux为crontab），如下
`*/2 * * * * cd /your/path/ExpressBot && python main.py`
即为两分钟运行一次

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

## 致谢 ##
* [coderfox/Kuaidi100API](https://github.com/coderfox/Kuaidi100API)
* [jaehee~임재희](https://twitter.com/GFW) 感谢你的大力调戏
* [ヨイツの賢狼ホロ](https://github.com/KenOokamiHoro) 感谢你的commits，我直接无耻的拉过来了。

## TODO ##
- [x] 这个机器人可以跟你聊天扯淡呢~
- [ ] SSL 证书问题

## License ##
GPL v2