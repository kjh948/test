# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from gtts import gTTS
from pygame import mixer
import time
import pyttsx
import subprocess

class r2d2Tts(object):
    def __init__(self, lang='ko', engine='google'):
        self.lang = lang
        if engine is not 'google':
            #use offline engine
            self.isGoogle = False
            self.offline_engine = pyttsx.init()
        else:
            self.isGoogle = True

    def speak(self,utt, isBlock=True):
        if self.isGoogle:
            tts = gTTS(text=utt, lang=self.lang)
            tts.save('response.mp3')
            mixer.init()
            mixer.music.load('response.mp3')
            mixer.music.play()
            if isBlock==True:
                while mixer.music.get_busy():
                   time.sleep(1)
        else:
            try:
                cmdln = 'espeak '
                cmdln = cmdln + '"' + utt + '"'
                # call external program ro take a picture
                subprocess.check_call([cmdln], shell=True)
            except subprocess.CalledProcessError, e:
                print "Ping stdout output:\n", e.output

    #self.offline_engine = pyttsx.init()
            #self.offline_engine.say(utt)
            #self.offline_engine.runAndWait()
