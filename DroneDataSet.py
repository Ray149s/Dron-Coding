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

def videoRecorder():
    vidId = 4
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    ## cv2.VideoWriter(filename, codec being used, frame per sec,  )
    count = 0 
    #DState = tello.get_current_state()
    DStateM = [] 
    video = cv2.VideoWriter(f'Resources/Vid/'+str(vidId)+'.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height)) # DStateMF = str

   
    while keepRecording:
        
        video.write(frame_read.frame)
        DStateM.insert(count, [tello.get_current_state()])
        time.sleep(1 / 30)
        # print(DStateM, "\n") 
        count+=1


        cv2.imshow("Current video ",frame_read.frame)       ## Gives window to display image
        cv2.waitKey(1) 
        

    video.release()
    count = 0
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

    if kp.getKey("z"): 
        ## The imwrite saves an image to a specific file
        ## f is for file location
        ## {time.time()}.jpg is the name of the image file we are saving
        ## The first time is calling on the library the second time is calling on the fuction
        ## time function prints the current time/date which is a uniqu name and good for what we are doing
        ## ,img tells the function what we are saving 
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',frame_read.frame)
        ## time.sleep allows us to click the take picture button z and not take 15 pictures with one click
        time.sleep(0.3)


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

    ### if kp.getKey("z"): 


    tello.send_rc_control(lr, fb, ud, yv)



