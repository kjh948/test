import sys
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time

import os
from multiprocessing import Process, Queue
import logging

logging.basicConfig(level=logging.INFO)

min_size = (15,15)
image_scale = 2
haar_scale = 1.2
min_neighbors = 5
haar_flags = 0

class r2d2Vision(object):
    def __init__(self, mode='face', path = 'resources/haarcascade_frontalface_alt2.xml'):
        self.model = cv2.CascadeClassifier(path)
        self.vs = VideoStream(src=0).start()
        #self.vs = cv2.VideoCapture(0)
        # self.vs.set(3, 320)
        # self.vs.set(4, 240)
        time.sleep(2.0)
        self.fps = FPS().start()
        self.isDetected = None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        fx = 0.5
        if fx != 1.0:
            gray = cv2.resize(gray, (0, 0), fx=fx, fy=fx)
        faces = self.model.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=min_neighbors,
            minSize=min_size,
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        if faces is not None:
            for (x, y, w, h) in faces:
                sc = int(1/fx)
                cv2.rectangle(frame, (sc*x, sc*y), (sc*(x + w), sc*(y + h)), (0, 255, 0), 2)
        cv2.imshow("video", frame)
        self.fps.update()
        return faces

    def process(self, delay=0):
        t = cv2.getTickCount()
        time.sleep(delay)
        frame = self.vs.read()
        ret = self.detect(frame)
        print "time taken for detection = %gms" % ((cv2.getTickCount() - t) / (cv2.getTickFrequency() * 1000.))
        return ret

    def loop(self, msg=None, delay=0):
        while 1:
            ret = self.process(delay)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if len(ret)>0:
                self.isDetected = ret
                #msg.put(ret)
            else:
                self.isDetected = None
                #msg.put(None)

if __name__ == "__main__":
    msg = Queue()
    vis = r2d2Vision()

    delay = 0.0
    #proc = Process(target=vis.loop, args=(msg,delay,))
    proc = Process(target=vis.loop())

    proc.start()
    while 1:
        try:
            res = msg.get(timeout=1)
            if res is not None:
                print(res)
                #logging.info('detected')
        except:
            break
    proc.join()
    vis.fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(vis.fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(vis.fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vis.vs.stop()
