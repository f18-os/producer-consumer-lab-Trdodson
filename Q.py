#A simple, fixed buffer for producerConsumer.py provided by instructor.

class Q:
    def __init__(self, initArray = [], maxSize = 10):
        self.a = []
        self.a = [x for x in initArray]
        
    def put(self, item):
        if len(self.a) > 10:
            print("ERROR: Out of bounds!")
            return
        
        self.a.append(item)

    def get(self):
        a = self.a
        item = a[0]
        del a[0]
        return item

    def __repr__(self):
        return "Q(%s)" % self.a
