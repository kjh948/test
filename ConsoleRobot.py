#-*- coding: euc-kr -*-

import os
import subprocess  # needed to run external program raspistill 
#import serial
import time
from os import path
import sys
#sys.setdefaultencoding("utf-8")
import google_query as q

command_case = {
        "앞으로",   
        "뒤로",   
        "좌로",
        "우로",
        }
   
#ser = serial.Serial('/dev/ttyUSB0', 9600)


#cmdln='./gtts_run.sh '
#cmdln = cmdln + '"나는 로봇입니다. 준비되었습니다."'
# call external program ro take a picture
#subprocess.check_call([cmdln], shell=True)

import speech_recognition as sr


"""
# obtain audio from the microphone
subprocess.check_call(['adinrec -lv 1000 -zc 200 out.wav'], shell=True,stderr=subprocess.STDOUT)

WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "out.wav")

# use "test.wav" as the audio source
r = sr.Recognizer()
with sr.WavFile(WAV_FILE) as source:
    audio = r.record(source) # read the entire WAV file

print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
"""

r = sr.Recognizer()
m = sr.Microphone()

WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "out.wav")

with m as source:
    #print("Calibrating!")
    #r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
    #print("Done")
    #audio = r.listen(m)
    #str=r.recognize_google(audio,language = "ko-KR")
    #print(str)
    while 1:
        print("Say something!")
        #audio = r.listen(m)
        try:
            subprocess.check_call(['adinrec -lv 1000 -zc 200 out.wav'], shell=True,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, e:
            print "Ping stdout output:\n", e.output
        with sr.WavFile(WAV_FILE) as source:
            audio = r.record(source) # read the entire WAV file
        try:        
            str=r.recognize_google(audio,language = "ko-KR")
            print(str)
        except:
            print "can't understand"
        os.remove('out.wav')
        '''
        cmdln='./gtts_run.sh '
        cmdln = cmdln + '"네 알겠습니다."'
        # call external program ro take a picture
        subprocess.check_call([cmdln], shell=True)
        '''
        res = q.query(str.encode('euc-kr'))
        
        if len(res) > 0:
            res = res[0].decode('utf-8')
            print res
            cmdln='./gtts_run.sh '
            cmdln = cmdln + '"'+res+ '"'
            # call external program ro take a picture
            subprocess.check_call([cmdln], shell=True)
        else:
            print 'no results'

        #cmdln='./gtts_run.sh '
        #cmdln = cmdln + '"'+str+ '"'
        # call external program ro take a picture
        #subprocess.check_call([cmdln], shell=True)

#        if u"앞으로" in str:
#            cmdln='./gtts_run.sh '
#            cmdln = cmdln + '"네네네네"'
#            # call external program ro take a picture
#            subprocess.check_call([cmdln], shell=True)
#            #ser.write('f')
#            time.sleep(1)
#            #ser.write('s')
#        elif u"뒤로" in str:
#            cmdln='./gtts_run.sh '
#            cmdln = cmdln + '"네네네네"'
#            # call external program ro take a picture
#            subprocess.check_call([cmdln], shell=True)
#            #ser.write('b')
#            time.sleep(1)
#            #ser.write('s')
#        elif u"좌로" in str:
#            cmdln='./gtts_run.sh '
#            cmdln = cmdln + '"네네네네"'
#            # call external program ro take a picture
#            subprocess.check_call([cmdln], shell=True)
#            #ser.write('l')
#            time.sleep(1)
#            #ser.write('s')
#        elif u"우로" in str:
#            cmdln='./gtts_run.sh '
#            cmdln = cmdln + '"네네네네"'
#            # call external program ro take a picture
#            subprocess.check_call([cmdln], shell=True)
#            #ser.write('r')
#            time.sleep(1)
#            #ser.write('s')    
#        elif(1):
#            cmdln='./gtts_run.sh '
#            cmdln = cmdln + '"무슨 말인지 모르겠습니다.."'
#            # call external program ro take a picture
#            subprocess.check_call([cmdln], shell=True)
