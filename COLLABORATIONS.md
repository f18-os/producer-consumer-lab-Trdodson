# Collaborations

* Thanks to Dr. Fruedenthal for code that captures from MP4,  encodes,
  decodes, and converts frames. Specifically, all functions within
  producerConsumer.py contains portions from:
  ~~~
  ExtractFrames.py
  ExtractAndDisplay.py
  ConvertToGrayscale.py
  ~~~
*
  https://www.geeksforgeeks.org/producer-consumer-solution-using-semaphores-java/
  - A java solution for producer-consumer involving semaphores. This solution
  helped me realize how to properly initialize my semaphores so that no thread
  consumes nor produces at the wrong time (i.e. consuming when nothing is
  in the queue, or producing when queue is full.)
