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
            self.oBuff.put(jpgImage)
            success,image = vidcap.read()
            print("Reading frame {} {} " .format(count,success))
            count += 1
            
        print ("Extraction finished!")
            
class Convert(Thread):
    def __init__(self, oBuff, cBuff):
        Thread.__init__(self, daemon=False)
        self.oBuff = oBuff
        self.cBuff = cBuff
        self.start()
    def run(self):
        count = 0
        while True:
            if not self.oBuff.empty():
                frame = self.oBuff.get()
                dImage = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(dImage, cv2.COLOR_BGR2GRAY)
                
                self.cBuff.put(img)
                print("Converted frame", count)
                count += 1
        print ("Conversion finished.")
            
class Display(Thread):
    def __init__(self, cBuff):
        Thread.__init__(self, daemon=False)
        self.cBuff = cBuff
        self.start()
    def run(self):
        count = 0
        while True:
            print("Displaying frame", count)
            img = self.cBuff.get()
            cv2.imshow("Sample", img)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
            count += 1
            
filename = 'clip.mp4'
outDir = 'frames'

if not os.path.exists(outDir):
    print("Creating 'frames' directory.")
    os.makedirs(outDir)

Extract(filename, buff1)
Convert(buff1, buff2)
Display(buff2)
