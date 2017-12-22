#!/usr/bin/python
# coding:utf-8

# ExpressBot - speech.py
# 2017/12/21 21:22
# Speech API handler
# reference: https://github.com/Uberi/speech_recognition

__author__ = 'Benny <benny@bennythink.com>'

from pydub import AudioSegment
import speech_recognition as sr


def convert(ogg_path, ogg_name):
    song = AudioSegment.from_ogg(ogg_path + ogg_name)
    wav_file = ogg_path + ogg_name[0:-4] + '.wav'
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
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


def voice_to_text(ogg_path, ogg_name):
    return recognition(convert(ogg_path, ogg_name))
