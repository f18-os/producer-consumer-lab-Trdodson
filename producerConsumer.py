#! /usr/bin/env python3

from threading import Thread, Lock 
import time

block = Lock()

class Extract(Thread):
    def __init__ (self):
        Thread.__init__(self, daemon=False)
    def run (self):
        while True:
            block.acquire()
            block.release()
            time.sleep(random.random())
            
class Convert(Thread):
    def run(self):
        while True:
            block.acquire()
            block.release()

            
class Display(Thread):
    def run(self):
        while True:
            block.acquire()
            block.release()


            
p = Extract()
p.start()
c = Convert()
c.start()
c2 = Display()
c2.start()
