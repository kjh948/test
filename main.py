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


def process_utterance():
    detector.interrupted = True
    isTriggered = False
    utt = asr.get_asr()
    print('asr results: ' + utt)
    response = brain.get_response(utt)
    if response.confidence < SCORE_THRE:
        #unmatchaed. go to google
        response = query(utt)
        if response: tts.speak(response)
    else:
        response = response.text
        print('bot results: ' + response)
        cmd = utt.split()
        if len(cmd) > 1:
            #response with command
            eval(cmd[1])
            tts.speak(cmd[2])
        else:
            tts.speak(response)

    detector.interrupted = False

wakeup_model = 'resources/thomas.pmdl'

isTriggered = False
def triggered():
    global isTriggered
    isTriggered = True

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Initialize ThreadedDetector object and start the detection thread
detector = snowboythreaded.ThreadedDetector(wakeup_model, sensitivity=0.8)
detector.start()

detector.start_recog(detected_callback=triggered,sleep_time=0.03)

while 1:
    try:
        if isTriggered>0:
            process_utterance()
    except (KeyboardInterrupt, SystemExit):
        detector.terminate()
        raise
    finally:
        exit(1)

