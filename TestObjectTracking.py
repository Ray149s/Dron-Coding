import cv2
from djitellopy import Tello
import cv2, time
import ColorDetection as CLD
import ContourDetection as CTD


################################################################################
################################################################################
width = 320 ## WIDTH OF THE IMAGE
height = 240 ## HEIGHT OF THE IMAGE
startCounter = 1 ## 0 FOR  FLIGHT 1 FOR TESTING
################################################################################
################################################################################

## Connecting to Tello Drone
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0


print(me.get_battery())




me.streamoff()
me.streamon()

      
        


while True: 
    ## Get the image form Tello
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    ## To go up in the beginning
    ## The first frame should be 0 if it is than this will run
    ## method for movement is in distance to be travled 
    if startCounter == 0:
        me.takeoff()
        me.move_left(20)
        me.rotate_clockwise(90)
        me.move_up(100)
        time.sleep(4)
        startCounter = 1

## Send velocity values to telllo
#    if me.send_rc_control:
#       me.send_rc_control(me.for_back_velocity, me.left_right_velocity, me.up_down_velocity, me.yaw_velocity,)

## Display Image
    cv2.imshow("MyResult", img)

# Set up to stop program when q is pressed

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        me.land()
        break

