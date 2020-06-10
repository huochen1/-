# -*- encoding: UTF-8 -*-
import os
import sys
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import yuyinhecheng
import yuyinshibie
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位采集
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
RECORD_SECONDS = 5  # 采样时长 定义为9秒的录音
WAVE_OUTPUT_FILENAME = "./myvoice.pcm"  # 采集声音文件存储路径
token = yuyinshibie.get_access_token()


def main():
    # 发送者默认设置
    FROM = '自己的qq邮箱'
    password = "smtp密码"#可以看看网上怎么用smtp协议发送邮件的
    smtp_server = "smtp.qq.com"

    # 根据语音提示输入音频，识别并返回结果

    TO = '接收者邮箱' + '@' + 'qq' + '.com'  # 由于不能识别特殊符号，所以就把接收邮箱内容分割输入

    name = '自己想'
    url = "http://tsn.baidu.com/text2audio?tex=请说主题&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
    os.system('mpg123 "%s"' % url)

    os.system('sudo arecord -D "plughw:1" -f S16_LE -r 16000 -d 5 /home/pi/email/pwm.wav')
    SUBJECT = yuyinshibie.asr_main("/home/pi/email/pwm.wav", token)
    url = "http://tsn.baidu.com/text2audio?tex=请说内容&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
    os.system('mpg123 "%s"' % url)
    os.system('sudo arecord -D "plughw:1" -f S16_LE -r 16000 -d 8 /home/pi/email/pwm.wav')
    text = yuyinshibie.asr_main("/home/pi/email/pwm.wav", token)

    def _format_addr(s):
        # 这个函数的作用是把一个标头的用户名编码成utf-8格式的，如果不编码原标头中文用户名，用户名将无法被邮件解码
        name, addr = parseaddr(s)
        return formataddr((Header(name, "utf-8").encode(), addr))
        # Header().encode(splitchars=';, \t', maxlinelen=None, linesep='\n')
        # 功能：编码一个邮件标头，使之变成一个RFC兼容的格式

    # 接下来定义邮件本身的内容
    msg = MIMEMultipart()
    msg["From"] = _format_addr("CC <%s>" % FROM)
    msg["To"] = _format_addr("%s <%s>" % (name, TO))
    msg["Subject"] = Header(SUBJECT, "utf-8").encode()
    # 定义邮件正文
    msg.attach(MIMEText(text, "plain", "utf-8"))

    # 接下来定义发送文件
    try:
        server = smtplib.SMTP(smtp_server, 25)
        server.login(FROM, password)
        server.sendmail(FROM, [TO], msg.as_string())
        server.quit()
        url = "http://tsn.baidu.com/text2audio?tex=发送成功&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
    except Exception, e:
        url = "http://tsn.baidu.com/text2audio?tex=发送失败&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
        os.system('mpg123 "%s"' % url)
        print
        str(e)


if __name__ == '__main__':
    main()
