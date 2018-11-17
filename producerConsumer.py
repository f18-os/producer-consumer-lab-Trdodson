#! /usr/bin/env python3
from threading import Thread, Lock 
import time
import cv2
import numpy as np
import base64
import queue
import os

block = Lock()
buff1 = queue.Queue(10)
buff2 = queue.Queue(10)
exFin = 0

class Extract(Thread):
    def __init__ (self, fileName, oBuff):
        Thread.__init__(self, daemon=False)
        self.fileName = fileName
        self.oBuff = oBuff
        self.start()
    def run (self):
        count = 0
        vidcap = cv2.VideoCapture(self.fileName)
        success,image = vidcap.read()
        print("Reading frame {} {} " .format(count,success))
        
        while success:
            success, jpgImage = cv2.imencode('.jpg',image)
            fText = base64.b64encode(jpgImage)
            self.oBuff.put(fText)
            success,image = vidcap.read()
            print("Reading frame {} {} " .format(count,success))
            count += 1
            
        print ("Extraction finished!")
        self.exFin = 1
            
class Convert(Thread):
    def __init__(self, oBuff, cBuff):
        Thread.__init__(self, daemon=False)
        self.oBuff = oBuff
        self.start()
    def run(self):
        count = 0
        while True:
            if not self.oBuff.empty():
                frameAsText = self.oBuff.get()
                rawImage = base64.b64decode(frameAsText)
                jImage = np.asarray(bytearray(rawImage),dtype=np.uint8)
                dImage = cv2.imdecode(jImage, cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(dImage, cv2.COLOR_BGR2GRAY)
                
                cv2.imshow("Sample", img)
                if cv2.waitKey(42) and 0xFF == ord("q"):
                    break
                
                # jpgImage = cv2.imencode('.jpg',img)
                #fText = base64.b64encode(jpgImage)
                #
                print("Converted frame", count)
                count += 1
                
        print ("Conversion finished.")
            
class Display(Thread):
    def __init__(self, oBuff):
        Thread.__init__(self, daemon=False)
    def run(self):
        pass

filename = 'clip.mp4'
outDir = 'frames'

if not os.path.exists(outDir):
    print("Creating 'frames' directory.")
    os.makedirs(outDir)

Extract(filename, buff1)
Convert(buff1, buff2)
