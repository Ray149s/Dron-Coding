## "as kp" allows us to shorten the amount typed when wanting to use KeyPressModule from KeyPressModule.blahblahblah to kp.blahblahblah
import math
from cv2 import destroyAllWindows

from djitellopy import tello
import KeyPressModule as kp
import numpy as np
import cv2
from time import sleep
import os
############ PARAMETERS ##################
# fSpeed = 117/10 ## Forward Speed in cm/s ruffly 12cm/s which is not (15cm/s was speed used for testing)
fSpeed = 200/10 ## Forward Speed in cm/s  ruffly 20cm/s        #######  ruffly 12cm/s which is not (15cm/s was speed used for testing)
aSpeed = 360/10 ## Angular Speed Degrees/s so the drone rotates at ruffly 36cm/s (50cm/s was speed used for testing)
interval = .06 ## We will take measurements with respect to .25 sec instead of 1 second like in the video
            ## TODO: See if you can ajust to be able grab more frames per sec as of right now .03 (1/30) fps is to fast for the program
            ## TODO: So we are going to be grabing a frames 15fps
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

points = [(0,0),(0,0)]
xyzList = [(0,0,0,0),(0,0,0,0)]
## creates lift thrust followed by hover thrust


##########################################
###########  Saving Files  ###############
## ! Important adjust the take so that you dont over right files
experiment_Take = 0
save_dir_Img = "C:/Users/User/Documents/school/Major Tracking/Research/REU/UCCS/Dron Coding/Prictice Files/Resorces/Mapping XYZ Images/"
save_dir_List = "C:/Users/User/Documents/school/Major Tracking/Research/REU/UCCS/Dron Coding/Prictice Files/Resorces/Mapping XYZ List/"
    
def create_dir(path):
    try: 
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name{path}")

## Accepts the variables from main and implements them as fallows in order To:
## Extract Frames from each video in path
## Create a directory for each video file to store each the frames of that video
## Create file names for each frame

def save_list(save_dir, list, take):
    ## Grabs the name of the video files in the video_path and assigns it to variable name 
    ##  by creating a list that first splits up the value in video_path by the \ in path 
    ##  then splits up things by . then grabbing the first element in the list generated 
    name = str(take) + "OdometryCoordinates"

    ## Creates the name for the new file to be created in the create_dir method by concatenating 
    ## value in save_dir sent from main with the value of variable name derived above
    save_path = os.path.join(save_dir, name)
    
    ## Creates the Directory
    create_dir(save_path)
    
    with open(f"{save_path}/{name}.csv", 'w') as f:  
        f.write("x,y,z,z-relative\n")
        for row in list:
            # print(row)
            Data4 = str(row).replace("[", "")
            Data3 = str(Data4).replace("]", "")
            Data2 = str(Data3).replace("(", "")
            Data1 = str(Data2).replace(")", "")
            Data = str(Data1).replace("'", "")
            f.write(Data + "\n")
            
    # np.save(f"{save_path}/{name}.npy", list)

def save_img(save_dir, img, take):
    ## Grabs the name of the video files in the video_path and assigns it to variable name 
    ##  by creating a list that first splits up the value in video_path by the \ in path 
    ##  then splits up things by . then grabbing the first element in the list generated 
    name = str(take) + "OdometryCoordinates"

    ## Creates the name for the new file to be created in the create_dir method by concatenating 
    ## value in save_dir sent from main with the value of variable name derived above
    save_path = os.path.join(save_dir, name)
    
    ## Creates the Directory
    create_dir(save_path)

    cv2.imwrite(f"{save_path}/{name}.jpg", img)
   


## check the key strokes applied to keyboard

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 20
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
        yaw += aInterval       #Chack previous value and ad to it.
    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): 
        me.land()
        sleep(3) 
        xyzList
        save_list(save_dir_List, xyzList, experiment_Take)
        save_img(save_dir_Img, img, experiment_Take)
        destroyAllWindows()
        quit()
        
    

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
                ## ( image, information, location, font, fontsize, color, font thickness )
    # cv2.putText(img, f'({(points[-1][0]-500)/ 100}, {(points[-1][1]-500)/100})m',            ## IN meters
    #             (points[-1][0] + 50, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, 
    #             (255, 0, 255), 1)

    cv2.putText(img, f'({(points[-1][0]-500)}, {-(points[-1][1]-500)})cm',            ## In cm
                (points[-1][0] + 50, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, 
                (255, 0, 255), 1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    
    img = np.zeros((1000, 1000, 3), np.uint8) ## Matrix of zeros that is 1k x 1k by 3 deep RGB values but in open cv we uses BRG not RGB 
                                             ## np.uint8 means values of this matrix will be unsigned integers than can me 8 bit
                                             ## 8 bit 2^8 which equals 256 so our values to be stored will range from 0-255
   
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
            points.append((vals[4], vals[5]))
            print("load points")
            xyzList.append(((points[-1][0]-500), -(points[-1][1]-500), str(me.get_state_field('h')), str(me.get_state_field('tof'))))
            print("load xyz")

    drawPoints(img, points) 
    print(points[-1])
    print(xyzList[-1])
    cv2.imshow("Output", img) # This opens the image in a window
    cv2.waitKey(1)  # this delays the closer so that end up not being able to see the mage


    
