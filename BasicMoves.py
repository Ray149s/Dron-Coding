# import djitellopy.tello
from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()

## Check battery percentage
print(me.get_battery())

## Take off
me.takeoff()

## Go up at a rate of 50 somethings
me.send_rc_control(0,0,70,0)
## Do so for 3 seconds
sleep(3)
## Go down at a rate of 25 somethings
me.send_rc_control(0,0,-25,0)
## Do so for 2 seconds
sleep(2)

## Make do directional movements
me.send_rc_control(0,0,0,0)
sleep(5)

## Land
me.land()
