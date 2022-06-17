## "as kp" allows us to shorten the amount typed when wanting to use KeyPressModule from KeyPressModule.blahblahblah to kp.blahblahblah
import math
from djitellopy import tello
import KeyPressModule as kp
import numpy as np
import cv2
from time import sleep

############ PARAMETERS ##################
fSpeed = 117/10 ## Forward Speed in cm/s  ruffly 12cm/s which is not (15cm/s was speed used for testing)
aSpeed = 360/10 ## Angular Speed Degrees/s so the drone rotates at ruffly 36cm/s (50cm/s was speed used for testing)
interval = 0.25 ## We will take measurements with respect to .25 sec instead of 1 second like in the video

dInterval = fSpeed*interval  ## distance traveled over the interval of time
aInterval = aSpeed *interval ## angle achieved over the interval of time
###########################################
x, y = 500, 500
a = 0
yaw = 0

## Calls the init function from the kp class
kp.init()

## Initializes variable containing communication frame work to be used in order to communicate  with Rizo drone
me = tello.Tello()

## Searches and connects script with Rizo drone
me.connect()

## prints battery life to console
print(me.get_battery())

points = [(0, 0), (0, 0)]
## creates lift thrust followed by hover thrust

## check the key strokes applied to keyboard

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global yaw, x, y, a
    d = 0           ## We want distance to be reset every time but not the angle so we put distance inside and angle outside the getKeyboard Input.
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180  
    elif kp.getKey("RIGHT"): 
        lr = speed
        d = -dInterval
        a = 180
    if kp.getKey("UP"): 
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"): 
        fb = -speed
        d = -dInterval
        a = -90
    if kp.getKey("w"): 
        ud = speed

    elif kp.getKey("s"): 
        ud = -speed
    
    if kp.getKey("a"): 
        yv = -aspeed
        yaw -= aInterval  #Chack previous value and ad to it. 

    elif kp.getKey("d"): 
        yv = aspeed
        yaw += aInterval
    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land();sleep(3) #Chack previous value and ad to it.

    sleep(interval)
    a += yaw
    ## The following two lines requierd the import of math in order to work
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))


    return [lr, fb, ud, yv, x, y]
   
def drawPoints(img, points):
    for point in points:                                   ## Recognize that we have point and points they are not the same and not differentiating them will cause the code not to work
                                                           ## I mistakenly used points everywhere in the following code and it caused the if statement on line 105
                                                           ## and the drawPoints function on line 108 to not work
        cv2.circle(img, point, 5,(0, 0, 255), cv2.FILLED)  ## 20 is the size of the circle dot being filled, cv2.circle defines the shape
                                                           ## image field the shapes starting location is determined by  x and y cv2.FILLED in with red(0,0,255)
    
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
   
    cv2.putText(img, f'({(points[-1][0]-500)/ 100}, {(points[-1][1]-500)/100})m', 
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, 
                (255, 0, 255), 1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    
    img = np.zeros((1000, 1000, 3), np.uint8) ## Matrix of zeros that is 1k x 1k by 3 deep RGB values but in open cv we uses BGR not RGB 
                                             ## np.uint8 means values of this matrix will be unsigned integers than can me 8 bit
                                             ## 8 bit 2^8 whits equals 256 so our values to be stored will range from 0-255
   
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
            points.append((vals[4], vals[5]))

    drawPoints(img, points) 

    cv2.imshow("Output", img) # This opens the image in a window
    cv2.waitKey(1)  # this delays the closer so that end up not being able to see the mage
    

    
