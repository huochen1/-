#!/usr/bin/env python
# encoding: utf-8
#
# 利用热词唤醒后使用百度语音识别api识别语音指令,然后匹配操作指令.如关灯,开灯操作.
###　使用snowboy的多个热词唤醒,效果会更好,而且不需要网络. 有空测试.

"""
@version: ??
@author: chm
@time: 2020/6/1
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import pyaudio
import wave
import pygame
import snowboydecoder
import signal
import yuyinshibie
import yuyinhecheng
from light import Light
import RPi.GPIO as GPIO
from aip import AipSpeech
import tianqi
import receive
import send
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''#百度语音申请的

APIClient = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

interrupted = False
token = yuyinshibie.get_access_token()
# 定义采集声音文件参数
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位采集
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
RECORD_SECONDS = 5  # 采样时长 定义为9秒的录音
WAVE_OUTPUT_FILENAME = "./myvoice.pcm"  # 采集声音文件存储路径
ef controllpwm(speed):
    # atexit.register(GPIO.cleanup）
    #os.system('cd /home/pi/Desktop&&./start on')​  # 这句应该可以不要
    servopin = 32  # 用到树莓派哪个口
    GPIO.setmode(GPIO.BOARD)  # 设置模式
    GPIO.setup(servopin, GPIO.OUT, initial=False)  # 设置32为输出
    p = GPIO.PWM(servopin, 50)  # 50HZ #设置32为PWM 频率50Hz
    p.start(0)
    p.ChangeDutyCycle(speed)
    time.sleep(0.02)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# _*_ coding:UTF-8 _*_
# @author: zdl
# 实现离线语音唤醒和语音识别，实现一些语音交互控制

# 导入包

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


#  回调函数，语音识别在这里实现
def callbacks():
    global detector
    #  关闭snowboy功能
    detector.terminate()
    url = "http://tsn.baidu.com/text2audio?tex=你好&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
    os.system('mpg123 "%s"' % url)
    #  开启语音识别
    os.system('sudo arecord -D "plughw:1" -f S16_LE -r 16000 -d 3 /home/pi/Desktop/pwm.wav')
    info = yuyinshibie.asr_main("/home/pi/Desktop/pwm.wav", token)

    if '打开卧室灯'.encode("utf-8") in info:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, True)
        url = "http://tsn.baidu.com/text2audio?tex=卧室灯已打开&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)

    elif '关闭卧室灯'.encode("utf-8") in info:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, False)
        url = "http://tsn.baidu.com/text2audio?tex=卧室灯已关&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
    elif '打开客厅灯'.encode("utf-8") in info:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(12, True)
        url = "http://tsn.baidu.com/text2audio?tex=客厅灯已开&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
    elif '关闭客厅灯'.encode("utf-8") in info:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(12, False)
        url = "http://tsn.baidu.com/text2audio?tex=客厅灯已关&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)

    elif '开风扇'.encode("utf-8") in info:
        servopin = 32
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servopin, GPIO.OUT, initial=False)
        p = GPIO.PWM(servopin, 50)
        p.start(0)
        p.ChangeDutyCycle(45)
        url = "http://tsn.baidu.com/text2audio?tex=风扇已开&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
    elif '二档'.encode("utf-8") in info:
        servopin = 32
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servopin, GPIO.OUT, initial=False)
        p = GPIO.PWM(servopin, 50)
        p.start(0)
        p.ChangeDutyCycle(95)
        yici = '风扇已开二档'
        url = "http://tsn.baidu.com/text2audio?tex=" + yici + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
    elif '关风扇'.encode("utf-8") in info:
        servopin = 32
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servopin, GPIO.OUT, initial=False)
        p = GPIO.PWM(servopin, 50)
        p.start(0)
        erci = '风扇已关'
        url = "http://tsn.baidu.com/text2audio?tex=" + erci + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)

    elif '播放稻香'.encode("utf-8") in info:
        pygame.mixer.init()
        filename = '/home/pi/Music/' + '稻香' + '.mp3'
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=0)

    elif '暂停播放'.encode("utf-8") in info:
        pygame.mixer.init()
        pygame.mixer.music.stop()

        pygame.mixer.music.stop()
    elif '播放七里香'.encode("utf-8") in info:
        pygame.mixer.init()
        filename = '/home/pi/Music/' + '七里香' + '.mp3'
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=0)
    elif '播放天气预报'.encode("utf-8") in info:
        tianqi.weather()
    elif '我要发送邮件'.encode("utf-8") in info:
        send.main()
    elif '最近一封邮件'.encode("utf-8") in info:
        receive.get_mail()

        # 打开snowboy功能
    wake_up()  # wake_up —> monitor —> wake_up  递归调用


# 热词唤醒
def wake_up():
    global detector
    model = './resources/xiaoduxiaodu.pmdl'  # 唤醒词为 小度小度
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # 唤醒词检测函数，调整sensitivity参数可修改唤醒词检测的准确性
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... please say wake-up word:SnowBoy')

    # main loop
    # 回调函数 detected_callback=snowboydecoder.play_audio_file
    # 修改回调函数可实现我们想要的功能
    detector.start(detected_callback=callbacks,  # 自定义回调函数
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    # 释放资源
    detector.terminate()


if __name__ == '__main__':
    # 初始化pygame,让之后播放语音合成的音频文件
    pygame.mixer.init()
    p = pyaudio.PyAudio()

    wake_up()
