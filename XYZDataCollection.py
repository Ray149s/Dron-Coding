from distutils.file_util import write_file
from msilib.schema import File
from cv2 import destroyAllWindows
import numpy as np
import KeyPressModule as kp
import time, cv2
from threading import Thread
from djitellopy import Tello
from array import *
from numpy import *
import sys as program
from time import sleep
import os
import math

###########################################################
#################      Saving Files            ################
## ! Important adjust the take so that you dont over right files###

experiment_Take = 'p_108.360.10.15.34'

save_dir_Img  = "C:/Users/duena/OneDrive/Documents/Dron Coding/Resources/XYZ_Pose/Map_Images"
save_dir_Vid  = "C:/Users/duena/OneDrive/Documents/Dron Coding/Resources/XYZ_Pose/Vid"
save_dir_List = "C:/Users/duena/OneDrive/Documents/Dron Coding/Resources/XYZ_Pose/List/"
vidId = experiment_Take
    
#################################################################
##############################################################

##############################################
############ PARAMETERS ##################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE

font = cv2.FONT_HERSHEY_SIMPLEX
bottom_left_corner = (10, 450)

## ! SPEED
fFPS =.08
Srate = 1/20
FPS = 20
                                ## fSpeed = 117/10 ## Forward Speed in cm/s ruffly 12cm/s which is not (15cm/s was speed used for testing)
fSpeed = 200/10                 ## !If I want to go fastr cm/s this number must strink to calc correct position                                      Forward Speed in cm/s  ruffly 20cm/s        #######  ruffly 12cm/s which is not (15cm/s was speed used for testing)
aSpeed = 360/10                 ## Angular Speed Degrees/s so the drone rotates at ruffly 36cm/s (50cm/s was speed used for testing)
interval = fFPS                 ## We will take measurements with respect to .25 sec instead of 1 second like in the video
#FPS                                ## TODO: See if you can ajust to be able grab more frames per sec as of right now .03 (1/30) fps is to fast for the program
                                    ## TODO: So we are going to be grabing a frames 15fps
dInterval = fSpeed*interval     ## distance traveled over the interval of time
aInterval = aSpeed *interval    ## angle achieved over the interval of time

x, y = 500, 500
a=0 
yaw =0

keepRecording = True
#################################
##########################################

############## Lists #########################
points = [(0,0),(0,0)]
xyzList = []
DStateM2 = []
NavVal= []  
##############################################



## Calls the init function from the kp class
kp.init()

## Initializes variable containing communication frame work to be used in order to communicate  with Rizo drone
tello = Tello()

## Searches and connects script with Rizo drone
tello.connect()

tello.streamon()
# frame_read = tello.get_frame_read()
frame_read = tello.get_frame_read()
    

def videoRecorder():
    ## ! FPS  
        ## cv2.VideoWriter----->(                filename,                   codec being used,      frame per sec,   frame dimentions  )
    video = cv2.VideoWriter(f'C:/Users/duena/OneDrive/Documents/Dron Coding/Resources/XYZ_Pose/Vid/'+str(vidId)+'.avi', cv2.VideoWriter_fourcc(*'XVID'), FPS, (width, height)) 

    while keepRecording:
      
        myFrame = frame_read.frame 
        frameRet = cv2.resize(myFrame, (width, height))
        video.write(frameRet)
      
        #########################
        text = "Battery Life Pecentage: " + str(tello.get_battery()) + " Tello Temp: " + str(tello.get_temperature())
        #########################  
        
        ## Puttin drone battery life and temp on video display and displaying the feed
        #########################
        cv2.putText(frameRet, text, bottom_left_corner, font, .75, (0, 0, 255), 2)
        cv2.imshow("Current video ",frameRet)       ## Gives window to display image
        ##########################
        cv2.waitKey(1) ## TODO: Keep it or 86 it

    video.release()

recorder = Thread(target=videoRecorder)
recorder.start()
###time.sleep(5)



def create_dir(path):
    try: 
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name{path}")



def save_list(save_dir, xyzList, NavVal, DStateM2,  take):
    
    ## Graebing the number of frames in the video taken and assigning the value to var lenth to be used as a descriper saved in the next two files

    ## Grabs the name of the video files in the video_path and assigns it to variable name 
    ##  by creating a list that first splits up the value in video_path by the \ in path 
    ##  then splits up things by . then grabbing the first element in the list generated 
    length = len(xyzList)
    name = str(take) + "_OdometryCoordinates"

    ## Creates the name for the new file to be created in the create_dir method by concatenating 
    ## value in save_dir sent from main with the value of variable name derived above
    # save_path = os.path.join(save_dir, name)
    
    ## Creates the Directory
    create_dir(save_dir)
    

    i = 0
    r = 0
    count = 0
    ## * csv ontainig directional movement, drone pose, and state informationf from the expierement file seperated by colems and cleaned up for eays of use
    with open(save_dir+name+'.csv', 'w') as f:  
        f.write("Line #,Navigation Direction,Padding,x,y,z,z_Relative,mpry0,mpry1,mpry2,pitch,roll,yaw,vgx,vgy,vgz,templ,emph,tof,h,bat,baro,time,agx,agy,agz\n")
        
        for row in DStateM2:
            Data26 = str(row).replace("a",""   )
            Data25 = str(Data26 ).replace("b",""   )
            Data24 = str(Data25 ).replace("c",""   )
            Data23 = str(Data24 ).replace("d",""   )
            Data22 = str(Data23 ).replace("e",""   )
            Data21 = str(Data22 ).replace("f",""   )
            Data20 = str(Data21 ).replace("g",""   )
            Data19 = str(Data20 ).replace("h",""   )
            Data18 = str(Data19 ).replace("i",""   )
            Data17 = str(Data18 ).replace("l",""   )
            Data16 = str(Data17 ).replace("m",""   )
            Data15 = str(Data16 ).replace("o",""   )
            Data14 = str(Data15 ).replace("p",""   )
            Data13 = str(Data14 ).replace("r",""   )
            Data12 = str(Data13 ).replace("t",""   )
            Data11 = str(Data12 ).replace("v",""   )
            Data10 = str(Data11 ).replace("w",""   )
            Data9  = str(Data10 ).replace("x",""   )
            Data8  = str(Data9  ).replace("y",""   )
            Data7  = str(Data8  ).replace("z",""   )
            Data6  = str(Data7  ).replace("[",""   )
            Data5  = str(Data6).replace("{","" )
            Data4  = str(Data5).replace("'","" )
            Data3  = str(Data4).replace(":","" )
            Data2  = str(Data3).replace("}","" )
            Data1  = str(Data2).replace("]","" )  
            Data    = Data1[28:]

            NavVall1 = str(NavVal[i]).replace("'","")
            NavVall2 = str(NavVall1).replace(",","")
            
            PosData4 = str(xyzList[r]).replace("[","")
            PosData3 = str(PosData4).replace("]", "")
            PosData2 = str(PosData3).replace("(", "")
            PosData1 = str(PosData2).replace(")", "")
            PosData  = str(PosData1).replace("'", "")
            Padding = "        "
            f.write(str(count)+"," + str(NavVall2) +",        ,"+ str(PosData) + str(Data) + "\n")
            count+=1
            i+=1
            r+=1       
    i = 0
    r = 0
    count = 0
    with open(save_dir+name+'2.csv', 'w') as f:  
        f.write("mpry0,mpry1,mpry2,pitch,roll,yaw,vgx,vgy,vgz,templ,emph,tof,h,bat,baro,time,agx,agy,agz,Padding,Line #,Padding,x,y,z,z_Relative,Navigation Direction\n")
        
        for row in DStateM2:
            Data26 = str(row).replace("a",""   )
            Data25 = str(Data26 ).replace("b",""   )
            Data24 = str(Data25 ).replace("c",""   )
            Data23 = str(Data24 ).replace("d",""   )
            Data22 = str(Data23 ).replace("e",""   )
            Data21 = str(Data22 ).replace("f",""   )
            Data20 = str(Data21 ).replace("g",""   )
            Data19 = str(Data20 ).replace("h",""   )
            Data18 = str(Data19 ).replace("i",""   )
            Data17 = str(Data18 ).replace("l",""   )
            Data16 = str(Data17 ).replace("m",""   )
            Data15 = str(Data16 ).replace("o",""   )
            Data14 = str(Data15 ).replace("p",""   )
            Data13 = str(Data14 ).replace("r",""   )
            Data12 = str(Data13 ).replace("t",""   )
            Data11 = str(Data12 ).replace("v",""   )
            Data10 = str(Data11 ).replace("w",""   )
            Data9  = str(Data10 ).replace("x",""   )
            Data8  = str(Data9  ).replace("y",""   )
            Data7  = str(Data8  ).replace("z",""   )
            Data6  = str(Data7  ).replace("[",""   )
            Data5  = str(Data6).replace("{","" )
            Data4  = str(Data5).replace("'","" )
            Data3  = str(Data4).replace(":","" )
            Data2  = str(Data3).replace("}","" )
            Data1  = str(Data2).replace("]","" )  
            Data    = Data1[28:]

            NavVall1 = str(NavVal[i]).replace("'","")
            NavVall2 = str(NavVall1).replace(",","")
            
            PosData4 = str(xyzList[r]).replace("[","")
            PosData3 = str(PosData4).replace("]", "")
            PosData2 = str(PosData3).replace("(", "")
            PosData1 = str(PosData2).replace(")", "")
            PosData  = str(PosData1).replace("'", "")
            Padding = "        "
            f.write(str(Data)+", " + "        , "+ str(count) + ",        , " +str(PosData) + ", " + str(NavVall2) + "\n")
            count+=1
            i+=1
            r+=1       
        f.write("The total number of frames for video clip "+str(vidId)+" is " + str(length) + " it was recorded at" + str(FPS) + " FPS.\n ")
        print("Saved csv file length is: ", length)



def save_img(save_dir, img, take):
# Grabs the name of the video files in the video_path and assigns it to variable name 
    ##  by creating a list that first splits up the value in video_path by the \ in path 
    ##  then splits up things by . then grabbing the first element in the list generated 
    name = str(take) + "_OdometryMap"

    ## Creates the name for the new file to be created in the create_dir method by concatenating 
    ## value in save_dir sent from main with the value of variable name derived above
    # save_path = os.path.join(save_dir, name)
    
    ## Creates the Directory
    create_dir(save_dir)

    cv2.imwrite(f"{save_dir}/{name}.jpg", img)



def drawPoints(img, points):
    z = tello.get_state_field('h')
    for point in points:                                    ## Recognize that we have point and points they are not the same and not differentiating them will cause the code not to work
                                                            ## I mistakenly used points everywhere in the following code and it caused the if statement on line 105
                                                            ## and the drawPoints function on line 108 to not work
        cv2.circle(img, point, 5,(0,225,0), cv2.FILLED)   ## 20 is the size of the circle dot being filled, cv2.circle defines the shape
                                                            ## image field the shapes starting location is determined by  x and y cv2.FILLED in with red(0,0,255)
    
    cv2.circle(img, points[-1], 8, (223,223,223 ), cv2.FILLED)
                ## ( image, information, location, font, fontsize, color, font thickness )
    # cv2.putText(img, f'({(points[-1][0]-500)/ 100}, {(points[-1][1]-500)/100})m',            ## IN meters
    #             (points[-1][0] + 50, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, 
    #             (255, 0, 255), 1)

    cv2.putText(img, f'( {(points[-1][0]-500)}, {-(points[-1][1]-500)}, {z} )cm',            ## In cm
                (points[-1][0] + 15, points[-1][1] + 15), cv2.FONT_HERSHEY_PLAIN, 1.25, 
                (225,0, 225), 2)


## ! SPEED
## TODO: Figure out what is going on with yaw and why when its adjustment in flights causes the values of x and y to loc up and no longe change when
## TODO:        Dealing with greater frames per second as 1/20 
## TODO:            Quick thought theory wold be when dealing with the same frame rate and travle rate as when you record 1/20 fps and travle at 20cm/s
## TODO                           you ed up with digets smaller than one and when put into the trig functions they get m uch smaller and cant be
## TODO                            rounded to an ineger produces a zero and x,y arent changed ths doesnt explain why it doesnt change again when 
## TODO                                 movingin a non yaw way. 
while keepRecording == True:
        ## ! SPEED
    def getKeyboardInput():
        lr, fb, ud, yv = 0, 0, 0, 0
        speed = 15
        aspeed = 34
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
            ud = speed + 30
        ## ! Added the 30

        elif kp.getKey("s"): 
            ud = -speed - 30
        ## ! Added the 30

        if kp.getKey("a"): 
            yv = -aspeed
            yaw -= aInterval  #Chack previous value and ad to it. 

        elif kp.getKey("d"): 
            yv = aspeed
            yaw += aInterval       #Chack previous value and ad to it.
        if kp.getKey("e"): 
            tello.takeoff()
        if kp.getKey("q"): 
            tello.land()
            sleep(5) 
            save_img(save_dir_Img, img, experiment_Take)
            save_list(save_dir_List, xyzList, NavVal, DStateM2,  experiment_Take)  
         
            # kp.quit()
            # cv2.destroyAllWindows()
            os._exit(0)
           

        sleep(fFPS)
        a += yaw
        ## The following two lines requierd the import of math in order to work
        x += int(d*math.cos(math.radians(a)))
        y += int(d*math.sin(math.radians(a)))

        return [lr, fb, ud, yv, x, y]


    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    
    img = np.zeros((1000, 1000, 3), np.uint8) ## Matrix of zeros that is 1k x 1k by 3 deep RGB values but in open cv we uses BRG not RGB 
                                            ## np.uint8 means values of this matrix will be unsigned integers than can me 8 bit
                                            ## 8 bit 2^8 which equals 256 so our values to be stored will range from 0-255

    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
            points.append((vals[4], vals[5]))
            print("load points")
            

    NavVal1 = "0"; NavVal2 = "0"; NavVal3 = "0"; NavVal4 = "0"; NavVal5 = "0"; NavVal6 = "0"; NavVal7 = "0"; NavVal8 = "0"
    Left = "LEFT"; Right = "RIGHT";  Foward = "UP"; Backward = "DOWN";  Up = "w";  Down = "s"; YarLeft = "a"; YarRight = "d"
    if kp.getKey(Left):     NavVal1 = "Left"                                                      
    elif kp.getKey(Right):    NavVal2 = "Right"                            
    if kp.getKey(Foward):   NavVal3 = "Foward"                         
    elif kp.getKey(Backward): NavVal4 = "Backward"                    
    if kp.getKey(Up):       NavVal5 = "Up"                                   
    elif kp.getKey(Down):     NavVal6 = "Down"     
    if kp.getKey(YarLeft):  NavVal7 = "YarLeft"  
    elif kp.getKey(YarRight): NavVal8 = "YarRight" 
    
    # xyzList.append(((points[-1][0]-500), -(points[-1][1]-500), str(tello.get_state_field('h')), str(tello.get_state_field('tof'))))
    xyzList.append(((vals[4]-500), -(vals[5]-500), str(tello.get_state_field('h')), str(tello.get_state_field('tof'))))
    NavVal.append([NavVal1,NavVal2,NavVal3,NavVal4,NavVal5,NavVal6,NavVal7,NavVal8])
    DStateM2.append([tello.get_current_state()])
    time.sleep(Srate)
                       
    drawPoints(img, points) 
    print(points[-1])
    print(xyzList[-1])
    print(len(NavVal),len(xyzList),len(DStateM2))
    cv2.imshow("Output", img) # This opens the image in a window
    cv2.waitKey(1)  # this delays the closer so that end up not being able to see the mage ## ? Maybe this lines and or line 240 are the problem
destroyAllWindows()
quit()
######################################################################################################################




