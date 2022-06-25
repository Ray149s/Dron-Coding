import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()

## Check battery percentage
print(me.get_battery())

#Image racognition gives us all frames one by one
me.streamon()

me.takeoff()
me.send_rc_control(0,0,20,0)
time.sleep(2.5)

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0] ## perportional p, derivative d, and integreal i, you can change these values to try and get better results
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources\haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 7)  ## for some reason the .detectMultiScale is not recognized

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    ## Checking for values in myFaceListArea to make sure we dont try to do calculations on nothing
    if len(myFaceListArea) !=0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0,0],0]

def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w//2 ## x is the value of our object in this case the face and w//2 is the center of the image
    speed = pid[0]*error + pid[1] *(error - pError)  ## changing the sencitivity of our errer by the dumber value 
    speed = int(np.clip(speed,-100,100))


   
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    
    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)

    me.send_rc_control(0, fb, 0, speed)
    
    return error



cap = cv2.VideoCapture(0) ## I had alote of truble getting this code to execute I would get errors but they didn't point to this line
                          ## What it ended up being was that I was telling the computer to use the second cammera by inputing
                          ## cv2.VideoCapture(1) instead of cv2.VideoCapture(0)
while True:
    #_, img = cap.read()
    img = me.get_frame_read().frame  ## Gives them the individual image frame 
    img = cv2.resize(img,(w,h))
    img, info = findFace(img)
    pError = trackFace(me, info, w, pid, pError)
    # print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
