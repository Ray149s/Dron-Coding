from distutils.file_util import write_file
import numpy as np
import KeyPressModule as kp
import time, cv2
from threading import Thread
from djitellopy import Tello
from array import *



tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    ## cv2.VideoWriter(filename, codec being used, frame per sec,  )
    count = 0
    DState = tello.get_current_state()
    DStateM = [[any]]
    video = cv2.VideoWriter(f'Resources/Vid/{time.time()}.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    DStateMF = str
    while keepRecording:
        video.write(frame_read.frame); DStateM.insert(count,[DState]); count = count+1
        time.sleep(1 / 30)
        print(DStateM)
        for row in DStateM:

        write_file(f'Resources/StateData/DStateM.txt', DStateM)
        # DStateMF.close()
        cv2.imshow("Current video ",frame_read.frame)       ## Gives window to display image
        cv2.waitKey(1) 
        

    video.release()

# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video

recorder = Thread(target=videoRecorder)

recorder.start()
time.sleep(10)
# tello.move_up(100)
# tello.rotate_counter_clockwise(360)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     keepRecording = False
#     recorder.join()
keepRecording = False
recorder.join()

