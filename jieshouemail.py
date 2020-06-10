# -*- coding:utf-8 -*-
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
from aip import AipSpeech
import time
import sys
reload(sys)
import yuyinhecheng
import yuyinshibie
import pyaudio
sys.setdefaultencoding('utf-8') #设置默认编码为utf-8，如不设置，代码中出现中文会报错
token = yuyinshibie.get_access_token()
import os
#""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#语音播报，传入的参数：
#text：语音播报内容
#flag：保存的文件名
def tts(text,flag):
    result  = client.synthesis(text, 'zh', 1, {
        'vol': 5,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('./'+flag, 'wb') as f:
            f.write(result)
    print(2)


def get_mail():
    # 设置默认接收邮箱，使用的是qq邮箱
    email = ''
    passwd = ''
    pop_server = 'pop.qq.com'

    server = poplib.POP3_SSL(pop_server, '995')
    print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(passwd)
    # print('Message:%s. Size:%s' % server.stat())

    # 返回所有邮件编号
    resp, mails, octets = server.list()

    index = len(mails)  # 所有邮件数
    if index < 1:
        return None
    resp, lines, octets = server.retr(index)
    # 获取最新一封邮件，索引号是从1开始的。lines存储了邮件的原始文本的每一行

    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # print(msg_content)

    # 把邮件内容解析为Massage对象，用来解析邮件
    msg = Parser().parsestr(msg_content)
    server.quit()
    print_info(msg)


def guess_charset(my_msg):
    charset = my_msg.get_charset()
    if charset is None:
        content_type = my_msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
        return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
        return value
def print_info(my_msg,indent=0):
    if indent==0:
        #邮件的From,To,Subject存在于跟根对象上
        for header in ['From','Subject']:
            value=my_msg.get(header,'')
            if value:
                if header=='Subject':
                    #解码Subject字符串
                    value=decode_str(value)
                    print('主题：%s' %value)
                    if (value==None):
                        url = "http://tsn.baidu.com/text2audio?tex=无主题&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)
                    else:
                        url = "http://tsn.baidu.com/text2audio?tex=主题是&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)
                        url = "http://tsn.baidu.com/text2audio?tex=" + value + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)
                else:
                    #解码Email地址
                    hdr,addr=parseaddr(value)
                    name=decode_str(hdr)
                    print('发送者：%s' %name)
                    if (name==None):
                        url = "http://tsn.baidu.com/text2audio?tex=发送者未知&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)
                    else:
                        url = "http://tsn.baidu.com/text2audio?tex=发送者是&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)
                        url = "http://tsn.baidu.com/text2audio?tex=" + name + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                        os.system('mpg123 "%s"' % url)

    #若还有其他对象（如文本内容、附件等）则继续打印
    if my_msg.is_multipart():
        parts=my_msg.get_payload()
        for n,part in enumerate(parts):
            print('%spart %s' %(' ' * indent,n))
            print('%s-----------------------------------' % ' ' * indent)
            print_info(part, indent + 1)

    #文本内容
    else:
        content_type = my_msg.get_content_type()
        if content_type == 'text/plain' :
            content = my_msg.get_payload(decode=True)
            #检测文本编码
            charset = guess_charset(my_msg)
            if charset:
                content = content.decode(charset)
                print('Text: %s' % (content))
                if (content==None):
                    url = "http://tsn.baidu.com/text2audio?tex=邮件内容是无&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                    os.system('mpg123 "%s"' % url)
                else:
                    url = "http://tsn.baidu.com/text2audio?tex=邮件内容是&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                    os.system('mpg123 "%s"' % url)
                    url = "http://tsn.baidu.com/text2audio?tex=" + content + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
                    os.system('mpg123 "%s"' % url)



if __name__ == '__main__':
    get_mail()