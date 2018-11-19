# Collaborations

* Thanks to Dr. Fruedenthal for code that captures from MP4,  encodes,
  decodes, and converts frames. Specifically, all functions within
  producerConsumer.py contains portions from:
  ~~~
  ExtractFrames.py
  ExtractAndDisplay.py
  ConvertToGrayscale.py
  ~~~
  
* https://www.geeksforgeeks.org/producer-consumer-solution-using-semaphores-java/
  - A java solution for producer-consumer involving semaphores. This solution
  helped me realize how to properly initialize my semaphores: no matter what
  order the threads execute, put() always happens first, and a put-then-get
  patten is enforced.


* https://stackoverflow.com/questions/45169559/how-to-make-worker-threads-quit-after-work-is-finished-in-a-multithreaded-produc
  - Gave me the idea of putting -1 in queue to indicate that the work is done.

  
* Q.py is a rough custom queue class provided by Dr. Freudenthal.

