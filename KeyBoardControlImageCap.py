## "as kp" allows us to shorten the amount typed when wanting to use KeyPressModule from KeyPressModule.blahblahblah to kp.blahblahblah
from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import cv2
import time

## Calls the init function from the kp class
kp.init()
## Initializes variable containing communication frame work to be used in order to communicate  with Rizo drone
me = tello.Tello()

## Searches and connects script with Rizo drone
me.connect()

## prints battery life to console
print(me.get_battery())
## creates lift thrust followed by hover thrust

global img

me.streamon()

## check the key strokes applied to keyboard
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed
    
    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed
    
    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed
    
    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv = speed

    
    if kp.getKey("q"): me.land(); time.sleep(3)
    if kp.getKey("e"): me.takeoff()


    if kp.getKey("z"):
        ## The imwrite saves an image to a specific file
        ## f is for file location
        ## {time.time()}.jpg is the name of the image file we are saving
        ## The first time is calling on the library the second time is calling on the fuction
        ## time function prints the current time/date which is a uniqu name and good for what we are doing
        ## ,img tells the function what we are saving 
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        ## time.sleep allows us to click the take picture button z and not take 15 pictures with one click
        time.sleep(0.3)

    return [lr, fb, ud, yv]
   

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img= me.get_frame_read().frame  ## Gives them the individual image frame 
    img= cv2.resize(img,(360,240))  ## Resize the image in order to process faster keeping frame small makes Processing faster
    cv2.imshow("Image", img)       ## Gives window to display image
    cv2.waitKey(1)                  ## With out the wait key the Image window will shutdown before we can see the image so we give it a delay of 1 mili sec

