import KeyPressModule as kp
import time, cv2
from threading import Thread
from djitellopy import Tello
from time import sleep

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter(f'Resources/Vid/{time.time()}.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)
        cv2.imshow("Live Video", frame_read)       ## Gives window to display image
        cv2.waitKey(1) 

    video.release()

# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video

recorder = Thread(target=videoRecorder)
recorder.start()

# tello.takeoff()
# tello.move_up(100)
# tello.rotate_counter_clockwise(360)
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
    if kp.getKey("q"): me.land();sleep(3); keepRecording = False; recorder.join()

    return [lr, fb, ud, yv]
   

while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
# tello.land()

#keepRecording = False
#recorder.join()


#####################################################################################
# ## Image capture for data set
# from djitellopy import tello
# import cv2
# import time
# me = tello.Tello()
# me.connect()

# ## Check battery percentage
# print(me.get_battery())

# #Image racognition gives us all frames one by one
# me.streamon()

# while True:
#         img= me.get_frame_read().frame  ## Gives them the individual image frame 
#         img= cv2.resize(img,(360,240))  ## Resize the image in order to process faster keeping frame small makes Processing faster
#         cv2.imshow("Image ", img)       ## Gives window to display image
#         cv2.waitKey(1) 

#         if(cv2.waitKey(1) & 0xFF == ord('c')):
#             cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)

#         if(cv2.waitKey(1) & 0xFF == ord('q')):
#             img.release()
#             cv2.destroyAllWindows()

