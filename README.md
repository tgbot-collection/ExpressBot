ExpressBot
==

帮你查快递的Telegram机器人！

## 部署方法 ##
需要部署在可以访问Telegram API的服务器上（或者设置代理）
### 准备环境 ###
```
git clone https://github.com/BennyThink/ExpressBot
cd ExpressBot
pip install -r requirements.txt
```
### 配置 ###
修改`config.py`中的TOKEN，以nohub或screen运行`main.py`
```
nohup python main.py
# 或者
screen -S tgbot
python main.py
```
将timer加入到任务计划中（Linux为crontab），如下
`*/2 * * * * python /your/path/ExpressBot/main.py`
即为两分钟运行一次

## TODO ##
* 修复潜在bug
* 优化，提高效率
* 改善易用性

## License ##
GPL v2