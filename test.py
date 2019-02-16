# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import snowboythreaded
import sys
import signal
import time

stop_program = False

from asr import r2d2Asr
from tts import r2d2Tts
from chatbot import r2d2Bot
from google_query import query
from robot import r2d2Robot

SCORE_THRE = 0.6

asr = r2d2Asr(ambient=True)
tts = r2d2Tts()
brain = r2d2Bot()
robot = r2d2Robot()

isTriggered = False
def triggered():
    global isTriggered
    isTriggered = True

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

wakeup_model = 'resources/thomas.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Initialize ThreadedDetector object and start the detection thread
detector = snowboythreaded.ThreadedDetector(wakeup_model, sensitivity=0.8)
detector.start()

detector.start_recog(detected_callback=triggered,sleep_time=0.03)

while 1:
    while(isTriggered):
        pass
    detector.interrupted = True
    isTriggered = False
    utt = asr.get_asr()
    print('asr results: ' + utt)
    response = brain.get_response(utt)
    if response.confidence < SCORE_THRE:
        response = query(utt)
    else:
        response = response.text
        print('bot results: ' + response)
    if response: tts.speak(response)

    detector.interrupted = False

threaded_detector.terminate()