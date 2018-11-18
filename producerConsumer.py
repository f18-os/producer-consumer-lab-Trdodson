#! /usr/bin/env python3
# A simple producer-consumer program - it extracts videos, converts them to grayscale, and then displays them. Some code from ExtractAndDisplay.py and ConvertToGrayscale.py. See COLLABORATIONS.md for details.  

from threading import Thread, Semaphore  
import cv2
import queue

eBlock = Semaphore(1) # Init to 1 to ensure img is produced first! 
cBlock = Semaphore(0) # Init to 0 so converter waits for extract.
cBlock2 = Semaphore(1) # Init to 1 so grayscale img is produced first!
dBlock = Semaphore(0) # Init to 0 so nothing is displayed 'till converter produced something.
eFinished = 0 # A flag for when extraction is finished!

conQueue = queue.Queue(10) # Extract-to-convert queue.
dispQueue = queue.Queue(10) # Convert-to-display queue.

# Extracts frames from mp4 file, encodes them as jpg, and places them in queue.
class Extract(Thread):
    def __init__ (self, fileName, oBuff):
        Thread.__init__(self, daemon=False)
        self.fileName = fileName
        self.oBuff = oBuff
        self.start()
    def run (self):
        global eFinished
        count = 0
        vidcap = cv2.VideoCapture(self.fileName)
        success,image = vidcap.read()
        print("Extracting frame {} {} " .format(count,success))

        # Encode & extract frames 'till there are no more to extract
        while success:
            success, jpgImage = cv2.imencode('.jpg',image)
            
            eBlock.acquire() # Make sure it's okay to produce - acquire lock!
            self.oBuff.put(jpgImage)
            cBlock.release() # Give permission to consume.
                
            success,image = vidcap.read()
            print("Extracting frame {} {} " .format(count,success))
            count += 1
            
        print ("Extraction finished!")
        eFinished = 1

# Convert frames to grayscale and places them in second queue. 
class Convert(Thread):
    def __init__(self, oBuff, cBuff):
        Thread.__init__(self, daemon=False)
        self.oBuff = oBuff
        self.cBuff = cBuff
        self.start()
    def run(self):
        count = 0
        while True:
            cBlock.acquire() # Get permission to consume.
            frame = self.oBuff.get()
            eBlock.release() # Give permission to produce
            
            dImage = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED) # Decode the frame.
            img = cv2.cvtColor(dImage, cv2.COLOR_BGR2GRAY) # Make it gray!

            cBlock2.acquire() # Get permission to produce.
            self.cBuff.put(img)
            dBlock.release() # Give permission to consume.
                    
            print("Converted frame", count)
            count += 1

# Display the converted frames in the second queue.
class Display(Thread):
    def __init__(self, cBuff):
        Thread.__init__(self, daemon=False)
        self.cBuff = cBuff
        self.start()
    def run(self):
        count = 0
        while True:
            dBlock.acquire() # Get permission to consume.
            print("Displaying frame", count)
            img = self.cBuff.get()
            cBlock2.release() # Give permission to produce.

            # Display the images as 24 fps.
            cv2.imshow("Sample", img)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
            count += 1

# Specify file and start the threads.
filename = 'clip.mp4'
Extract(filename, conQueue)
Convert(conQueue, dispQueue)
Display(dispQueue)
