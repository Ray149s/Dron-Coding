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


frameWidth = width
frameHeight = height

## Setting up parameters to be used to display text video frame display screen 
font = cv2.FONT_HERSHEY_SIMPLEX
bottom_left_corner = (10, 470)
######################################################################



## This function defines how we read the frames from the drones camera, creates an array to store drone state data,
##    rights drone state data to file, write video to a file
def videoRecorder():
    vidId = 00 #17
  
    count = 0 
    #DState = tello.get_current_state()
    DStateM = [] 
    
    ## cv2.VideoWriter(filename, codec being used, frame per sec,  )
    video = cv2.VideoWriter(f'Resources/Vid/'+str(vidId)+'.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height)) # DStateMF = str
    


    while keepRecording:
        ## Creating object to read frames from tello drones camera
        frame_read = tello.get_frame_read()
        ## Initializing the object as myFrame
        myFrame = frame_read.frame 
        ## Resizing the image to the parameters of width and height from above
        frameRet = cv2.resize(myFrame, (width, height))
    
        text = "Battery Life Percentage: " + str(tello.get_battery()) + " Tello Temp: " + str(tello.get_temperature())
        
        video.write(frameRet)

        ## This records the drones state at a rate of 30 states/sec to match the frame rate of video 
        ## So that when extracting frames from video I will have the drones state for each of the frames
        DStateM.insert(count, [tello.get_current_state()])
        time.sleep(1 / 30)
        # print(DStateM, "\n") 
        count+=1
        #########################
        #########################
        cv2.putText(frameRet, text, bottom_left_corner, font, .75, (0, 0, 255), 2)
        #########################
        #########################


       
        ############
        ## Gives window to display image
        cv2.imshow("Current video ",frameRet)       
        ############
        
        cv2.waitKey(1) 
        

    video.release()
    count = 0
    ## This writes the drones state (which was taken at 30 measures/sec in order to match the frame rate) from the DStateM
    ## array to a datafile for use later
    ## Separating the recorded data fore each recording by prefixing the data with four rows containing a "+"
    ##  and a row with the the video takes number ID given by vidId
    with open(f'Resources/StateData/testData.txt', 'a') as f:  
        f.write("\n")
        f.write("+ \n")
        f.write("+ \n")
        f.write("+ \n")
        f.write("\n")
        f.write("Video " + str(vidId) + " data: \n")
        for row in DStateM:
            # print(row)
            f.write(str(count) + str(row) + "\n")
            count+=1

        cap = cv2.VideoCapture(f'Resources/Vid/'+str(vidId)+'.avi')
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        f.write("The total number of frames for video clip "+str(vidId)+" is " + str(length) + ".\n \n")
        print(length)
       



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



