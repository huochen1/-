# -*- coding: utf-8 -*-
import sys, urllib2, json
import yuyinhecheng
import yuyinshibie
import os

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')  # 这个是解决合成中文文本的时候，Unicode和utf-8编码问题的，可以尝试注释掉会不会报错
token = yuyinshibie.get_access_token()


def weather():
    # 调用和风天气的API
    url = 'https://free-api.heweather.net/s6/weather/forecast?location=&key='#和风天气上申请key，城市随意

    req = urllib2.Request(url)
    resp = urllib2.urlopen(req).read()

    # 将JSON转化为Python的数据结构
    json_data = json.loads(resp)
    yi = json_data['HeWeather6'][0]

    # 获取城市
    city = yi['basic']['location']

    # 今天的天气
    today = yi['daily_forecast'][0]
    weather_day = today['cond_txt_d']
    weather_night = today['cond_txt_n']
    tmp_high = today['tmp_max']
    tmp_low = today['tmp_min']
    wind_dir = today['wind_dir']
    wind_sc = today['wind_sc']
    jintian = today['date']

    weather_forcast_txt = "%s今天天气%s转%s,最高气温%s摄氏度,最低气温%s摄氏度,风力%s,风向%s " % (
    city, weather_day, weather_night, tmp_high, tmp_low, wind_sc, wind_dir)

    print
    weather_forcast_txt

    url = "http://tsn.baidu.com/text2audio?tex=" + weather_forcast_txt + "&lan=zh&cuid=B8-27-EB-BA-24-14&ctp=1&tok=" + token + "&per=3"
    os.system('mpg123 "%s"' % url)


if __name__ == "__main__":
    weather()
