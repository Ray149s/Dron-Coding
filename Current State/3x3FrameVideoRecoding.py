from distutils.file_util import write_file
import numpy as np
import KeyPressModule as kp
import time, cv2
from threading import Thread
from djitellopy import Tello
from array import *
from numpy import *
import sys as program




kp.init()
tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

######################################################################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
deadZone =100
######################################################################
frameWidth = width
frameHeight = height


def videoRecorder():

    while keepRecording:
        #########################
        #########################
        myFrame = frame_read.frame 
        frameRet = cv2.resize(myFrame, (width, height))

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner = (10, 470)
        #########################
        #########################
        text = "Battery Life Percentage: " + str(tello.get_battery()) + " Tello Temp: " + str(tello.get_temperature())

        cv2.line   (frameRet,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
        cv2.line   (frameRet,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)
        cv2.circle (frameRet,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
        cv2.line   (frameRet, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
        cv2.line   (frameRet, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)
        cv2.putText(frameRet, text, bottom_left_corner, font, .75, (0, 0, 255), 2)
       
        ############
        cv2.imshow("Current video ",frameRet)       ## Gives window to display image
        ############
        
        cv2.waitKey(1) 
    
       


# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video

recorder = Thread(target=videoRecorder)
recorder.start()
###time.sleep(5)


## Keyboard control of the drone
## Speed is set to 50 cm/sec
speed = 50
while True:
    lr, fb, ud, yv = 0, 0, 0, 0
    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv = speed

    ## z key wll take a picture while in flight not necessary for the project but was a good exercise
    if kp.getKey("z"): 
        ## The imwrite saves an image to a specific file
        ## f is for file location
        ## {time.time()}.jpg is the name of the image file we are saving
        ## The first time is calling on the library the second time is calling on the function
        ## time function prints the current time/date which is a unique name and good for what we are doing
        ## ,img tells the function what we are saving 
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',frame_read.frame)
        ## time.sleep allows us to click the take picture button z and not take 15 pictures with one click
        time.sleep(0.3)

    ## This quit sequence is set up so that the video frame and drone state continue to get recorded and stay in sequence 
    ##  until the drone has landed and the feed has cut off
    if kp.getKey("q"): 
        tello.land()  
        time.sleep(5)       
        keepRecording = False; 
        recorder.join()
        kp.quit()
        tello.end()
        #cv2.destroyAllWindows()
        program.exit()

    ## creates lift thrust followed by hover thrust
    if kp.getKey("e"): tello.takeoff()

    ## Sends the thrust command given by keyboard input to the drone 
    tello.send_rc_control(lr, fb, ud, yv)



