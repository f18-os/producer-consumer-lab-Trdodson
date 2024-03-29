#! /usr/bin/env python3
# A simple producer-consumer program - it extracts videos, converts them to grayscale, and then displays them. Some code from ExtractAndDisplay.py and ConvertToGrayscale.py. See COLLABORATIONS.md for full attributions.  

from threading import Thread, Semaphore  
import cv2
from Q import Q

eBlock = Semaphore(1) # Init to 1 to initial frame is always produced first! 
cBlock = Semaphore(0) # Init to 0 so converter blocks 'till producer releases it.
cBlock2 = Semaphore(1) # Init to 1 so grayscale img is produced before display.
dBlock = Semaphore(0) # Init to 0 so display blocks 'till converter releases it.

conQueue = Q() # Extract-to-convert queue. Q object prints errors if exceeds 10 items.
dispQueue = Q() # Convert-to-display queue.

# Extracts frames from mp4 file, encodes them as jpg, and places them in queue.
class Extract(Thread):
    def __init__ (self, fileName, oBuff):
        Thread.__init__(self, daemon=False)
        self.fileName = fileName
        self.oBuff = oBuff
        self.start()
    def run (self):
        count = 0 # Count frames processed.
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
        cBlock.release() # Release the consumer once you're done!
        self.oBuff.put(-1) # Put a "cut off point" in the queue!

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

            if (frame is -1): # Nothing more to convert - stop!
                break
            
            dImage = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED) # Decode the frame.
            img = cv2.cvtColor(dImage, cv2.COLOR_BGR2GRAY) # Make it gray!

            cBlock2.acquire() # Get permission to produce.
            self.cBuff.put(img)
            dBlock.release() # Give permission to consume.
                    
            print("Converted frame", count)
            count += 1
            
        print("Conversion finished!")
        dBlock.release() 
        self.cBuff.put(-1) 

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

            if (img is -1): # Nothing more to display - stop!
                break
            
            # Display the images - 24 fps.
            cv2.imshow("Sample", img)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
            count += 1
        print("Finished displaying!")
        cv2.destroyAllWindows()
        
# Specify file and start the threads.
filename = 'clip.mp4'
Extract(filename, conQueue)
Convert(conQueue, dispQueue)
Display(dispQueue)
