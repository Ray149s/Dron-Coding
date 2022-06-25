# import djitellopy.tello
from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()

## Check battery percentage
print(me.get_battery())
text = "Battery Life Pecentage: " + str(me.get_battery()) + " Tello Temp: " + str(me.get_temperature())
## Take off
me.takeoff()
sleep(4)
xdist = me.get_mission_pad_distance_x()
ydist = me.get_mission_pad_distance_y()
zdist = me.get_mission_pad_distance_z()

print(xdist, ydist, zdist)
print(text)
me.rotate_clockwise(175)
me.go_xyz_speed(-50, -10, 10, 40)
sleep(4)


# ## Go up at a rate of 50 somethings
# me.send_rc_control(0,0,70,0)
# ## Do so for 3 seconds
# sleep(3)
# ## Go down at a rate of 25 somethings
# me.send_rc_control(0,0,-25,0)
# ## Do so for 2 seconds
# sleep(2)

# ## Make do directional movements
# me.send_rc_control(0,0,0,0)
# sleep(5)

## Land
me.land()
