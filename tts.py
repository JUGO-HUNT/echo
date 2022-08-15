#!/usr/bin /env python
# -*- coding :utf8 -*-

import json
import os
import requests
import datetime
#import sys
from aip import AipSpeech

from ymlhandle import cfg



#获取城市信息
def getCityInfo():
    geoUrl  = '{0}location=jiangning&adm=nanjing&key={1}'.format(cfg['qweather']['geoUrl'], cfg['qweather']['key'])
    geoData = requests.get(geoUrl).json()
    if int(geoData['code']) != 200:
        return cfg['qweather']['location']
    return [geoData['location'][0]['name'], geoData['location'][0]['id']]

#播报天气信息
def getWeather():
    cityInfo        = getCityInfo()[1]
    curWeatherUrl   = '{0}location={1}&key={2}'.format(cfg['qweather']['curWeatherUrl'], cityInfo, cfg['qweather']['key'])
    dailyWeatherUrl = '{0}location={1}&key={2}'.format(cfg['qweather']['dailyWeatherUrl'], cityInfo, cfg['qweather']['key'])
    airUrl          = '{0}location={1}&key={2}'.format(cfg['qweather']['airUrl'], cityInfo, cfg['qweather']['key'])
    
    curWeatherData      = requests.get(curWeatherUrl).json()
    dailyWeatherData    = requests.get(dailyWeatherUrl).json()
    airData             = requests.get(airUrl).json()

    if int(curWeatherData['code']) != 200:
        outstr = 'get current weather info failed!'
    elif int(dailyWeatherData['code']) != 200:
        outstr = 'get today weather info failed!'
    elif int(airData['code']) != 200:
        outstr = 'get air info failed!'
    else:
        outstr = '当前时间{1},{0}今天天气{2},最低气温{7}摄氏度,最高气温{8}摄氏度,体感{4}摄氏度,空气质量{5},PM2.5指数{6}.'.format(getCityInfo()[0],
                    datetime.datetime.now().strftime('%m月%d日 %H点%M分'), curWeatherData['now']['text'],
                    curWeatherData['now']['temp'], curWeatherData['now']['feelsLike'], airData['now']['category'],
                    airData['now']['pm2p5'], dailyWeatherData['daily'][0]['tempMin'], dailyWeatherData['daily'][0]['tempMax'])

    #outstr += specialDayRemind()                    
    return outstr 
    #cmdline = 'ilang "' + outstr + '"'
    #os.system(cmdline)

def specialDayRemind():
    love        = cfg['remind']['love']
    marriage    = cfg['remind']['marriage']
    wedding     = cfg['remind']['wedding']

    nowDay      = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
    loveDay     = datetime.datetime.strptime(love[0:10],"%Y-%m-%d")
    marriageDay = datetime.datetime.strptime(marriage[0:10],"%Y-%m-%d")
    weddingDay  = datetime.datetime.strptime(wedding[0:10],"%Y-%m-%d")

    outstr      = "今天是园园和蝈蝈相爱的第{0}天哦,距离你们结婚登记还有{1}天,注意需要提前30天预约登记，距离你们婚礼还有{2}天,今天又是美好的一天，加油".format((nowDay-loveDay).days, 
                        (marriageDay-nowDay).days, (weddingDay-nowDay).days)
    return outstr


#百度语音合成并播放
def txtToAudio(txtStr):    
    APP_ID      = cfg['tts&asr']['AppID']
    API_KEY     = cfg['tts&asr']['APIKey']
    SECRET_KEY  = cfg['tts&asr']['SecretKey']

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result  = client.synthesis(txtStr, 'zh', 1, {'vol': 5,})

    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)

    cmdline = 'mpg123 audio.mp3'
    os.system(cmdline)

if __name__ == '__main__':
    txtToAudio(getWeather())

#sys.exit()
#00 08 * * * . /etc/profile;/usr/bin/env python /home/pi/weatherVoice.py