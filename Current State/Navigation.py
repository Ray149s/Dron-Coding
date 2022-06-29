# import djitellopy.tello
from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()

## Check battery percentage and temp.
text = "Battery Life Percentage: " + str(me.get_battery()) + " Tello Temp: " + str(me.get_temperature())

## Take off
me.takeoff()
sleep(4)

print(text)

## Will send the drone to xyz position in relation to its current location
me.go_xyz_speed(-50, -10, 10, 40)
sleep(4)
me.land()
me.end()
