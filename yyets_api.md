# 人人影视 REST API
根据Windows版客户端抓包而来

## 主页搜索页面API,GET
```
http://pc.zmzapi.com/index.php?g=api/pv2&m=index&a=search&accesskey=519f9cab85c8059d17544947k361a827&limit=200&k=%E9%80%83%E9%81%BF
```
请求`http://www.zimuzu.tv`也是一样的结果。
k=为url编码的剧集名称，精确匹配
返回：
```
{
    "status": 1,
    "info": "",
    "data": [
        {
            "title": "《逃避可耻却有用》(NIGERUHA HAJIDAGA YAKUNITATSU)",
            "channel": "tv",
            "channel_cn": "电视剧",
            "id": "34812"
        },
        {
            "title": "《无法逃避》(Inescapable)[无法避免]",
            "channel": "movie",
            "channel_cn": "电影",
            "id": "29540"
        }
    ]
}
```

## 点击搜索结果，查看剧集信息，GET
```
http://pc.zmzapi.com/index.php?g=api/pv2&m=index&a=resource&accesskey=519f9cab85c8059d17544947k361a827&id=34812
```
id为上一步选择的ID，之后会返回全部下载链接，如果剧集有多个季，那么会在season中标明是第几季。
```
{
    "status": 1,
    "info": "",
    "data": {
        "detail": {
            "id": "34812",
            "cnname": "逃避可耻却有用",
            "enname": "NIGERUHA HAJIDAGA YAKUNITATSU",
            "channel": "tv",
            "channel_cn": "日剧",
            "category": "爱情",
            "close_resource": "2",
            "play_status": "本剧完结",
            "poster": "http://tu.zmzjstu.com/ftp/2016/1012/b_b6c308fdc8fae4ac151c98857f5653f2.jpg"
        },
        "list": [
            {
                "season": "101",
                "season_name": "单剧",
                "episodes": [
                    {
                        "episode": "11",
                        "episode_name": "第11集",
                        "files": {
                            "APP": [
                                {
                                    "name": "yyets://N=逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4|S=733784950|H=c464b9e32a999b417324b53cd92d2fbfa89b597a|",
                                    "format": "APP",
                                    "size": "",
                                    "way": "113",
                                    "address": "baofeng://N=逃避虽可耻但有用_11(720P)|G=3CF00D14DAD6962B8145DC86A98F9C5E04BF56C3|S=401611735|",
                                    "way_name": "其他源"
                                }
                            ],
                            "HR-HDTV": [
                                {
                                    "name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
                                    "format": "HR-HDTV",
                                    "size": "699.79MB",
                                    "way": "1",
                                    "address": "ed2k://|file|%E9%80%83%E9%81%BF%E5%8F%AF%E8%80%BB%E5%8D%B4%E6%9C%89%E7%94%A8.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4|733784950|51a18ead729a833f58264700b963113a|h=ncojnutlufhohfrl42xr7t2m6lqdwzjf|/",
                                    "way_name": "电驴ED2K下载"
                                },
                                {
                                    "name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
                                    "format": "HR-HDTV",
                                    "size": "699.79MB",
                                    "way": "999",
                                    "address": "https://d.miwifi.com/d2r/?url=ZWQyazovL3xmaWxlfCVFOSU4MCU4MyVFOSU4MSVCRiVFNSU4RiVBRiVFOCU4MCVCQiVFNSU4RCVCNCVFNiU5QyU4OSVFNyU5NCVBOC5OSUdFUlVIQS5IQUpJREFHQS5ZQUtVTklUQVRTVS5FcDExLkZpbmFsLkNoaV9KYXAuSERUVnJpcC4xMjgwWDcyMC1aaHVpeGluRmFuLm1wNHw3MzM3ODQ5NTB8NTFhMThlYWQ3MjlhODMzZjU4MjY0NzAwYjk2MzExM2F8aD1uY29qbnV0bHVmaG9oZnJsNDJ4cjd0Mm02bHFkd3pqZnwv&src=yyets&name=%E9%80%83%E9%81%BF%E5%8F%AF%E8%80%BB%E5%8D%B4%E6%9C%89%E7%94%A8.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
                                    "way_name": "小米路由器远程离线下载"
                                },
                                {
                                    "name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
                                    "format": "HR-HDTV",
                                    "size": "699.79MB",
                                    "way": "2",
                                    "address": "magnet:?xt=urn:btih:78930bae5efe391ee6bcc4c7dcfa237b05a493f0&tr=http://tracker.openbittorrent.com/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=udp://tr.cili001.com:6666/announce&tr=http://tracker.publicbt.com/announce&tr=udp://open.demonii.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=http://tr.cili001.com:6666/announce",
                                    "way_name": "BT磁力下载"
                                },
                                {
                                    "name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
                                    "format": "HR-HDTV",
                                    "size": "699.79MB",
                                    "way": "9",
                                    "address": "http://pan.baidu.com/s/1jHAM8aq",
                                    "way_name": "网盘"
                                }
                            ]
                        }
                    },
                  
                            ]
                        }
                    },
                            ]
                        }
                    }
                ]
            }
        ]
    }
}
```
如果有第二季的话，那么还会有个再多出来一个{}

## 最新发布的搜索，直接搜索到剧集，GET
```
http://www.zmzfile.com/file/search?keyword=%E9%80%83%E9%81%BF%E5%8F%AF%E8%80%BB
```
keyword=为url编码的剧集信息

返回：

```
[
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep01.Chi_Jap.HDTVrip.1280X720-ZhuixinFanV2.mp4",
        "file_size": 733967923,
        "fileid": "fa1a42ee8066da0aa2b66ca470814489160ad214",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=fa1a42ee8066da0aa2b66ca470814489160ad214"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep02.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629086728,
        "fileid": "d21a081cc6a32daa85310ca6aad81e378f0b736e",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=d21a081cc6a32daa85310ca6aad81e378f0b736e"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep03.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 628416378,
        "fileid": "9ac2a719d66b3626011c2d3366367a9d56c20e26",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=9ac2a719d66b3626011c2d3366367a9d56c20e26"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep04.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629037391,
        "fileid": "3274e38c1ba20493a0bf62d4f7c65bec651dc3d2",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=3274e38c1ba20493a0bf62d4f7c65bec651dc3d2"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep05.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629262958,
        "fileid": "30bb5f65bff74ebe60d848edd4748b3c3e7e76c7",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=30bb5f65bff74ebe60d848edd4748b3c3e7e76c7"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep06.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629239487,
        "fileid": "83f72df4cd440c22c8c5ab94b559773eb472c46d",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=83f72df4cd440c22c8c5ab94b559773eb472c46d"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep07.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629119647,
        "fileid": "bb2ff32f008d3d2e58371f34b83292ddde7b51e8",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=bb2ff32f008d3d2e58371f34b83292ddde7b51e8"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep08.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629207765,
        "fileid": "47e4573d0d72fa7d2394a377f467d0b352fce08f",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=47e4573d0d72fa7d2394a377f467d0b352fce08f"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep10.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 733930391,
        "fileid": "3c572ede5b41a2368d0f64071ea733592876344a",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=3c572ede5b41a2368d0f64071ea733592876344a"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep09.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 629132305,
        "fileid": "129e9e73d44ccf575afc70eecdd171732fc89329",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=129e9e73d44ccf575afc70eecdd171732fc89329"
    },
    {
        "file_name": "逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep11.Final.Chi_Jap.HDTVrip.1280X720-ZhuixinFan.mp4",
        "file_size": 733784950,
        "fileid": "c464b9e32a999b417324b53cd92d2fbfa89b597a",
        "url": "https://www.zmzfile.com:9043/rt/route?fileid=c464b9e32a999b417324b53cd92d2fbfa89b597a"
    }
]
```
对URL继续进行get，经过几轮重定向之后，即可得到真正的下载地址（根据你的IP重定向到不同的服务器）。
然后可以使用curl url -C - -Lv -o xxx.xxx下载。

**但是得到的文件是无法播放的，加密了。根据beyond compare的分析，文件中很多一部分都被加密了。**
**看样子需要逆向，最好能拿到源代码**

此时复制链接得到的大致如下：
yyets://N=逃避可耻却有用.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep01.Chi_Jap.HDTVrip.1280X720-ZhuixinFanV2.mp4|S=733967923|H=fa1a42ee8066da0aa2b66ca470814489160ad214|
**人人影视专用链是如何生成的？是否可以想办法逆向一下？**

电驴链接如下：
ed2k://|file|%E9%80%83%E9%81%BF%E5%8F%AF%E8%80%BB%E5%8D%B4%E6%9C%89%E7%94%A8.NIGERUHA.HAJIDAGA.YAKUNITATSU.Ep01.Chi_Jap.HDTVrip.1280X720-ZhuixinFanV2.mp4|733967923|7116a9dfb86fceed3f5b71604e48745f|h=ku7saiivihhc26hcbx4cjsplvkum62ho|/

磁力：
magnet:?xt=urn:btih:2a331028531d0254a2b1f30e55edf99b6b716e49&tr.1=http://tracker.openbittorrent.com/announce&tr.2=udp://tracker.openbittorrent.com:80/announce&tr.3=udp://tr.cili001.com:6666/announce&tr.4=http://tracker.publicbt.com/announce&tr.5=udp://open.demonii.com:1337&tr.6=udp://tracker.opentrackr.org:1337/announce&tr.7=http://tr.cili001.com:6666/announce

## 总结
基本上人人影视就提供这么几个API，很简单（可以说是简陋），但是也足够日常操作。
目前的工作重点之一是使用requests和json解析用户请求，正确返回对应的链接，二是还原被修改文件头的视频文件。

需要再次参考Telegram Bot文档。