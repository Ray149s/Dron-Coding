from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()

## Check battery percentage
print(me.get_battery())
print(me.get_current_state())

#Image racognition gives us all frames one by one
me.streamon()

## Because our camera is getting a contnues number of frames we need a while loop.
font = cv2.FONT_HERSHEY_SIMPLEX
bottom_left_corner = (10, 710)
#############################
#############################


while True:
        text = "Battery Life Pecentage: " + str(me.get_battery()) + " Tello Temp: " + str(me.get_temperature())
        img= me.get_frame_read().frame  ## Gives them the individual image frame 
        cv2.putText(img, text, bottom_left_corner, font, 1, (0, 0, 255), 2)
        img= cv2.resize(img,(360,240))  ## Resize the image in order to process faster keeping frame small makes Processing faster
        cv2.imshow("Image ", img)       ## Gives window to display image
        cv2.waitKey(1)                  ## With out the wait key the Image window will shutdown before we can see the image so we give it a delay of 1 mili sec

