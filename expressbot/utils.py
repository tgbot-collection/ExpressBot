#!/usr/bin/python
# coding:utf-8

# refuse message and not found message

__author__ = 'ヨイツの賢狼ホロ <horo@yoitsu.moe>'

import os
import random
import time

import speech_recognition as sr
from pydub import AudioSegment

from config import LOGGER
from db import Database

refuse_messages = [
    u'世上没有什么事情比必然与偶然更难懂了，就像要懂得木头人的爱恋之情一样困难。',
    u'咱活到现在，只要是让咱感到羞耻的人，咱都可以说出那个人的名字。这些名字当中还得再加上一个新的名字，那就是汝！',
    u'半吊子的聪明只会招来死亡。',
    u'人呐……在这种时候似乎会说『最近的年轻人……』呗。',
    u'真是的，汝惊慌失措时的样子还比较可爱呐。',
    u'因为汝是个大笨驴，如果没说出来，汝根本察觉不到呗。',
    u'在汝的脆弱心灵冻僵前，咱得赶紧用爪子好好抓上几道伤口才行。',
    u'汝不懂也罢。不……如果连汝也发现了，咱或许会有些困扰呗。',
    u'哼。俗话说一不做二不休，到时候咱也会很快地把汝吃进肚子里。',
    u'因为汝这种人说谎不眨眼的啊。一定会有的没的乱写一通。',
    u'汝认为所有人都要遵循汝的常识是吗？'
]

not_found_messages = [
    u'说谎的时候，重点不在于说谎的内容，而在于为何要说谎。',
    u'就算是咱，也有不能回答的事。',
    u'汝的脑筋虽然转得快，但经验还是不够。',
    u'就算如此，咱还是希望听到汝说出口。所以，重来一次。',
    u'又没有人起床，也只能睡觉呗。不睡觉只会觉得冷，而且还会饿肚子。'
]


def reply_refuse():
    return random.choice(refuse_messages)


def reply_not_found():
    return random.choice(not_found_messages)


# https://github.com/Uberi/speech_recognition
def ogg_to_wav(ogg_path):
    song = AudioSegment.from_ogg(ogg_path)

    wav_file = os.path.join(os.path.dirname(ogg_path), ogg_path.rsplit('\\')[-1].split('.')[0] + '.wav')
    song.export(wav_file, 'wav', 'pcm', '16k')
    return wav_file


def recognition(wav_file):
    r = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)
    # recognize speech using Google Speech Recognition
    try:
        return r.recognize_google(audio, language='cmn-Hans-CN')

    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio.4C7"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service.4C7; {0}".format(e)


def voice_to_text(ogg_path):
    v = ogg_to_wav(ogg_path)
    return recognition(v)


def msg_logger(fun):
    def wrapper(*args):
        res = fun(*args)

        if LOGGER:
            db = Database()
            sql = u'INSERT INTO msg VALUES (NULL ,?,?,?,?,?,?)'

            # user last name
            if args[0].chat.last_name is None:
                args[0].chat.last_name = ''

            log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args[0].date))
            p1 = (args[0].chat.id, args[0].message_id, args[0].chat.username,
                  args[0].chat.first_name + args[0].chat.last_name,
                  args[0].text, log_time)
            log_time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            p2 = (args[0].chat.id, args[0].message_id + 1, u'机器人', '', res, log_time2)

            db.con.cursor().executemany(sql, (p1, p2))
            db.con.commit()
            db.con.close()
        return res

    return wrapper


if __name__ == '__main__':
    re = r'C:\Users\Benny\AppData\Local\Temp\AwADBQADnAADJLjZVMv7E_goF5ubAg.ogg'
    print(voice_to_text(re))
