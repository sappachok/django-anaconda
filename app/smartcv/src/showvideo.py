'''
Using OpenCV takes a mp4 video and produces a number of images.
Requirements
----
You require OpenCV 3.2 to be installed.
Run
----
Open the main.py and edit the path to the video. Then run:
$ python main.py
Which will produce a folder called data with the images. There will be 2000+ images for example.mp4.
'''
import cv2
import numpy as np
import os
import time
from imutils.video import FPS

def show():
    # Playing video from file:
    cap = cv2.VideoCapture('train.mp4')
    fps = FPS().start()
    try:
        if not os.path.exists('video-images'):
            os.makedirs('video-images')
    except OSError:
        print ('Error: Creating directory of data')

    currentFrame = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        image = frame.copy()
        cv2.imshow('My First Object Detector', image)
        fps.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Saves image of the current frame in jpg file
        #name = './video-images/frame' + str(currentFrame) + '.jpg'
        #print ('Creating...' + name)
        #cv2.imwrite(name, frame)

        # To stop duplicate images
        #currentFrame += 1
        time.sleep(2000)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()