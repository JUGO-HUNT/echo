#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pyaudio
import wave
import numpy 

from ymlhandle import cfg


def recordMyVoice():
    #最小说话音量
    MIN_VOICE = 4000
    #最大说话音量，防止干扰出现30000+的音量
    MAX_VOICE = 28000
    #录音判断开始时间，前面的时间可能是回复的语音音量过大导致误判断
    START_SEC = 5
    #录音判断间隔，约等于8/16=0.5秒
    INTERVAL = 5
    #最大录音时间,16*10=160,十秒钟
    MAX_RECORD_TIME = 160
    temp = 20					#temp为检测声音值
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
 
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("录音开始")
 
    frames = []
    flag = False			#一重判断,判断是否已经开始说话，这个判断从第5个数字开始，防止前面数字大于30000的情况
    stat2 = False			#二重判断,第一次判断声音变小
    stat3 = False			#三重判断,第二次判断声音变小
    tempnum = 0				#tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0
    tempnum3 = 0
    while True:
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
        audio_data = numpy.frombuffer(data, dtype=numpy.short)
        #获取录音的音量
        temp = numpy.max(audio_data)
        #如果时间大于其实判断时间并且音量在正常范围之内
        if tempnum > START_SEC and flag == False and temp > MIN_VOICE and temp < MAX_VOICE:
            #判断出开始说话
            flag = True
        #如果已经开始说话，那么开始判断
        if(flag):
            #如果声音小于正常范围
            if temp < MIN_VOICE:
                #如果是stat2还是False状态，证明还未开始判断
                if stat2==False:
                    #时间点2和时间点3
                    tempnum2 = tempnum + INTERVAL
                    tempnum3 = tempnum + INTERVAL
                    #状态2开始变为True，说明第一次判断开始
                    stat2 = True
                #开始第二次判断，stat2为True表示已经第一次判断，超过第一次时间段开始第二次判断
                elif stat2 and stat3 == False and tempnum > tempnum2:
                    #已经超过了第一个时间段，那么stat3为True,这是第二次判断                   
                    stat3 = True
                #stat2和stat3都为True并且超过第二个时间段，这是最后一次判断
                if stat2 and stat3 and tempnum > tempnum3:
                    print("录音完毕")
                    #跳出循环
                    break
            else:
                #只要声音变大了，那么就重置状态
                stat2 = False
                stat3 = False
        #时间约1/16秒每次递增
        tempnum = tempnum + 1
        if tempnum > MAX_RECORD_TIME:				#超时直接退出
            print("录音结束")
             #跳出循环
            break
 
    stream.stop_stream()
    stream.close()
    p.terminate()
 
    wf = wave.open(cfg['tts&asr']['MyVoice'], 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    recordMyVoice()