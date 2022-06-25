import cv2
import numpy as np
import os
from djitellopy import tello

orb = cv2.ORB_create(nfeatures=1000)
path = 'Resources/Images/LandingPadImgs/'

############################
############################ 
## For Importing images

images = []
classNames= []
##grabs the names of all files in the directory specified
myList = os.listdir(path)
#print(myList)
## Prints out the number of items in myList which is the number of items in the specified directory
print('Total Classes Detected', len(myList))

## for class in myList take image from file and append it to images array
## for class in myList take the name of each image split the image name from the . jpg at the . keep element that of list jenerated by split, in this case [0] index gives the name
for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

############################
############################


## We want to find all the discripters of the images we should only have to do this once and we can do this outside of the while loop

## sending find descripter method our images
## we declar our list
## we loop through for all the images that we have
## we us orb.detectAnd Compute  to find the key points and descripptor for the images
def findDes(images):
    desList=[]
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList

## this function will determin the match srength of the item being percieved by the cammera and the images in the file
## by defining thress hold the way we have we give it the defalt value of 15 but allow the user to adjust when using
def findID(img, desList, thres = 12):
    ## des2 descripter 2 is the descripter of the current frame
    ## des1 descripter 1 is the name of the image files in LandingPadImgs
    kp2, des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher()
    ## Declaring new list that will stoor the number of good matches it is finding for each of the images
    matchList=[]
    ## This variable is going to carry the index of the file that was determend to have the highest liklyhood of beeing a match with the image the cammera is seeing we cant
    ## We cant put its initial value as a 0 or posiive number because thoughs all exist as indexes of the file names
    finalVal = -1
    ## Sometimes our matcher will not determin a match in this case we need to catch this error with a try catch as fallows
    try:
        ## We are going to loop through all the descripters des1 and match them with des2
        for des in desList:
            ## knnMatch takes descritpter 1 and descripter 2 and the K value which gives us 2 values to compare, and gives us all the matches that it can find. 
            matches = bf.knnMatch(des,des2,k=2)
            good=[]
            for m,n in matches:
                ## Whenever the distance between the values we get our low we will say it is a good match when the values between are high then we will say its a bad match. 
                ## depending on results we can adjust the .75 number
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
           
    except:
        pass
    print(matchList)
    if len(matchList) !=0:
        if max(matchList) > thres:
            ## matchList.index finds the index of the max value (max(matchList)) finds the max value
            finalVal = matchList.index(max(matchList))
    return finalVal
    
## we now call on the findDes method
desList = findDes(images)
print(len(desList))

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

cap = cv2.VideoCapture(0)
while True: 

    ## success and img are equal to cap.read()
    img2 = me.get_frame_read().frame 
    imgOriginal = img2.copy()
    ## Converts img2 to gray scale
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ## calling methed that compares what the cammera is seenig and what the we have in our files
    id = findID(img2,desList)
    if id !=-1:
        ## loading id into classNames[] gets the corisponding index of the name of file in clasName to the image that was determind to be mostlikly what is being seen by cammera
        cv2.putText(imgOriginal, classNames[id], (50,50),cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255),2)
       


    cv2.imshow('img2', imgOriginal)  ## If we had used img2 instead of imgOriginal than we would have seen a grayscale camera feed displayed
    cv2.waitKey(1)


