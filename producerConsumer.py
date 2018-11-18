#! /usr/bin/env python3
# A simple producer-consumer program - it extracts videos, converts them to grayscale, and then displays them. Some code from ExtractAndDisplay.py and ConvertToGrayscale.py. See COLLABORATIONS.md for details.  

from threading import Thread, Semaphore  
import cv2
import queue

block = Semaphore(1) # Handles blocking for extract-to-convert queue
block2 = Semaphore(1) # Handles blocking for convert-to-display queue.
buff1 = queue.Queue(10) # Extract-to-convert queue.
buff2 = queue.Queue(10) # Convert-to-display queue.

# Extracts frames from mp4 file, encodes them as jpg, and places them in queue.
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
        print("Extracting frame {} {} " .format(count,success))

        # Encode & extract frames 'till there are no more to extract
        while success:
            success, jpgImage = cv2.imencode('.jpg',image)
            
            if self.oBuff.empty(): # Stop everyone else if you've got nothing for them!
                block.acquire()
                
            self.oBuff.put(jpgImage)
            
            if not self.oBuff.empty(): #Let everyone run once there's something in the queue.
                block.release()
                
            success,image = vidcap.read()
            print("Extracting frame {} {} " .format(count,success))
            count += 1
            
        print ("Extraction finished!")

# Convert frames to grayscale. 
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
                dImage = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED) # Decode the frame.
                img = cv2.cvtColor(dImage, cv2.COLOR_BGR2GRAY) # Make it gray!

                # If you got nothing for the displayer, stop everything 'till you do!
                if self.cBuff.empty():
                    block2.acquire()
                    
                self.cBuff.put(img)

                # When you got something, let everyone resume!
                if not self.cBuff.empty():
                    block2.release()
                    
                print("Converted frame", count)
                count += 1
                
        print ("Conversion finished.")

# Display the converted frames!
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

Display(buff2)
Convert(buff1, buff2)
Extract(filename, buff1)
