## "as kp" allows us to shorten the amount typed when wanting to use KeyPressModule from KeyPressModule.blahblahblah to kp.blahblahblah
from djitellopy import tello
import KeyPressModule as kp
from time import sleep

## Calls the init function from the kp class
kp.init()
## Initializes variable containing communication frame work to be used in order to communicate  with Rizo drone
me = tello.Tello()
## Searches and connects script with Rizo drone
me.connect()
## prints battery life to console
print(me.get_battery())
## creates lift thrust followed by hover thrust
## me.takeoff()

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

    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land();sleep(3)

    return [lr, fb, ud, yv]
   

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
