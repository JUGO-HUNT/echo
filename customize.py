#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import random
import time

def selfDefinedBehavior(asrTxt):
    
    if '播放' in asrTxt and '音乐' in asrTxt:
        musicOn()
    elif '关闭' in asrTxt and '音乐' in asrTxt:
        musicOff()
    elif '关闭' in asrTxt and '系统' in asrTxt:
        echoExit()
    elif '关机' in asrTxt :
        powerOff()







def musicOn():
    musicOff()
    fileNameList = os.listdir('/home/pi/Music')
    fileName = fileNameList[random.randint(0,len(fileNameList) - 1)]
    cmdline = 'nohup mpg123 ' + '/home/pi/Music/'+ "'" + fileName  + "'" + ' > /dev/null 2>&1 &'
    os.system(cmdline)
 
def musicOff():
    isRunStr = str(os.popen("ps -ef | grep mpg123 | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
    if isRunStr=='pi':
        os.system("ps -ef | grep mpg123 | grep -v grep | awk '{print $2}' | xargs kill -9")
 
def echoExit():
    os.system("ps -ef | grep demo.py | grep -v grep | awk '{print $2}' | xargs kill -9")

def powerOff():
    os.system("sudo poweroff")