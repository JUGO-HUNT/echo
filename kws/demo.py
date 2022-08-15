import snowboydecoder
import sys
import signal
import os


sys.path.append("../")
import record
from ymlhandle import cfg
import asr_json
import tts
import tuling
import customize 

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def self_callbacks():
    global detector
 
    snowboydecoder.play_audio_file()
    cmdline = 'mpg123 ' + cfg['kws']['AwakeVoice']
    os.system(cmdline)
 
    #  关闭snowboy功能
    detector.terminate()

    #  开启语音识别
    record.recordMyVoice()
    asr_json.asr()
    if cfg['asr_result']['res']=='success':
        customize.selfDefinedBehavior(cfg['asr_result']['txt'])
        if cfg['tuling']['switchOn'] ==  'on':
            res = tuling.tuling(cfg['asr_result']['txt'])
            print(res)
            tts.txtToAudio(res)    

    # 打开snowboy功能
    wake_up()    # wake_up —> monitor —> wake_up  递归调用


def wake_up():
    # if len(sys.argv) == 1:
    #     print("Error: need to specify model name")
    #     print("Usage: python demo.py your.model")
    #     sys.exit(-1)
        
    global detector
    #model = sys.argv[1]
    model = '/home/pi/echo/kws/pmdl/echo.pmdl'

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=self_callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
    detector.terminate()


if __name__ == '__main__':
    wake_up()