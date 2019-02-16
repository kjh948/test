# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import snowboydecoder
import sys
import signal
import os
import collections
import time

from asr import r2d2Asr
from tts import r2d2Tts
from chatbot import r2d2Bot
from google_query import query
from robot import r2d2Robot

SCORE_THRE = 0.6

asr = r2d2Asr(ambient=False)
tts = r2d2Tts()
brain = r2d2Bot()
robot = r2d2Robot()


interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

wakeup_model = 'resources/thomas.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(wakeup_model, sensitivity=0.6)


def mainloop():
    #tts.speak('thomas')
    #return True

    buf_size = detector.detector.NumChannels() * detector.detector.SampleRate() * 5
    detector.ring_buffer._buf = collections.deque(maxlen=buf_size)
    snowboydecoder.play_audio_file()

    utt = asr.get_asr()
    print('asr results: ' + utt)
    response = brain.get_response(utt)
    if response.confidence < SCORE_THRE:
        response = query(utt)
    else:
        response = response.text
        print('bot results: ' + response)
    if response: tts.speak(response)


# main loop

detector.start(detected_callback=mainloop,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
detector.terminate()