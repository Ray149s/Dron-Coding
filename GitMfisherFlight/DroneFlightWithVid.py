# Using the Tello drone, this program demonstrates how to
# grab pictures and display them to a window as well as how
# to capture key presses in order to command the drone to
# translate. Using the send_rc_control() method because
# the other methods are not working at this time
#
# This program uses OpenCV to grab the images and capture key presses

import cv2
from djitellopy import tello
import time

# create drone object and connect to it
drone = tello.Tello()
drone.connect()

# flag to control main loop
keepRunning = True

# turn on video stream and get the image
# according to documentation - get the BackgroundFrameRead object
# from the camera drone. Then call backgroundFrameRead.frame to get
# the actual frame received by the drone, doing that in the main loop
drone.streamon()
print("Battery = " + str(drone.get_battery()))

readFrame = drone.get_frame_read()

while(keepRunning):

    img = readFrame.frame       # get actual frame from drone

    # display a window with title "Drone" and render the picture
    # that img points to
    cv2.imshow("Drone", img)
#################################################################
    speed = 50
    lr, fb, ud, yv = 0, 0, 0, 0 
    userInput = cv2.waitKey(1) & 0xff
    
    if(userInput == ord('q')):
        ## turn off video stream, land the drone, close windows and quit
        drone.streamoff()
        drone.land()
        cv2.destroyAllWindows()
        keepRunning = False
    elif(userInput == ord('t')):
        ## takeofft
        drone.takeoff()
    elif(userInput == ord("a")): 
        lr = -speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif(userInput == ord("d")): 
        lr = speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("w")): 
        fb = speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("s")): 
        fb = -speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("i")): 
        ud = speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("k")): 
        ud = -speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("j")): 
        yv = -speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(.1)
        drone.send_rc_control(0, 0, 0, 0)
    elif (userInput == ord("l")): 
        yv = speed
        drone.send_rc_control(lr, fb, ud, yv)
        time.sleep(1)
        drone.send_rc_control(0, 0, 0, 0)
    
    
#################################################################
    ## get user key press (the number 1 is the number of milliseconds to delay)
    ## the hexadecimal number 0xff is simply grabbing the last byte that the
    ## method waitKey() is returning. The Ampersand (&) is the bitwise AND operator
    
    # userInput = cv2.waitKey(1) & 0xff
    # if(userInput == ord('q')):
    #     ## turn off video stream, land the drone, close windows and quit
    #     drone.streamoff()
    #     drone.land()
    #     cv2.destroyAllWindows()
    #     keepRunning = False
    # elif(userInput == ord('t')):
    #     ## takeoff
    #     drone.takeoff()
    # elif(userInput == ord('w')):
    #     ## move forward
    #     drone.send_rc_control(0,50,0,0)
    #     time.sleep(2)
    #     drone.send_rc_control(0,0,0,0)
    # elif (userInput == ord('s')):
    #     ## move backward
    #     drone.send_rc_control(0, -50, 0, 0)
    #     time.sleep(2)
    #     drone.send_rc_control(0, 0, 0, 0)
###################################################################    
# shutdown all the windows
print("Landing ...")