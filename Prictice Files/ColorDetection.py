import numpy as np
import cv2
import numpy as np
import ImageStacker as IS

## Here we are definging the displayed video feed size, initiolizing the display
frameWidth = 640
frameHeight  = 480
## determining image source
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


## We need track bars in order to ajust and find the min and max HSV valuse that best fit our desierd useage
## Here we creat those track bars and the fnction empty() which is a necesary perramiter for creatTrackbar
def empty(a):
    pass

cv2.namedWindow('HSV')
cv2.resizeWindow("HSV",640,240)
## in opencv we have values of hue from 0-179  so we are putting those values in the track bar, empty represents the function that should run with this track bar as its interface 
cv2.createTrackbar("HUE MIN" ,"HSV" , 0, 179, empty)
cv2.createTrackbar("HUE MAX" ,"HSV" , 179, 179, empty)
cv2.createTrackbar("SAT MIN" ,"HSV" , 0, 255, empty)
cv2.createTrackbar("SAT MAX" ,"HSV" , 255, 255, empty)
cv2.createTrackbar("VALUE MIN" ,"HSV" , 0, 255, empty)
cv2.createTrackbar("VALUE MAX" ,"HSV" , 255, 255, empty)

## Iterates and gives s the outut of each frame that is stored in img varaible 
while True:
    ## calling the feed for image frames
    _, img = cap.read()

    ## BGR to HSV easier to work with for humans to work with hue = color, saturation = clearity, value = how bright
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Getting the values of the numbers that are being ajustied in the track bar
    h_min = cv2.getTrackbarPos("HUE MIN" ,"HSV" )
    h_max = cv2.getTrackbarPos("HUE MAX" ,"HSV" )
    s_min = cv2.getTrackbarPos("SAT MIN" ,"HSV" )
    s_max = cv2.getTrackbarPos("SAT MAX" ,"HSV" )
    v_min = cv2.getTrackbarPos("VALUE MIN" ,"HSV")
    v_max = cv2.getTrackbarPos("VALUE MAX" ,"HSV")
    print(h_min)


    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    ## only want objects that are within our range
    mask = cv2.inRange(imgHsv, lower, upper)
    ## what we are saying is we only want the valuses that are in both arrays the rest you can skip
    result = cv2.bitwise_and(img, img, mask = mask)

    ## Mask has only one channel but img, and result are 3 channel so we cannot stack unless we make 3 channel aswell
    ## we suse cv2.cvtColor  cv2.COLOR_GRA2BGR to do so now we can ad mask to the hSTack peramiters bellow
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    ##Stacking our windows into one window make easyer to work with we are stacking original image window and results window together
    
    hStack = IS.stackImages(0.5, [img, mask, result])
    
    
    ## Displays difernt windows
    # cv2.imshow("Original", img)
    # cv2.imshow('HSV Color Space', imgHsv)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('Results', result)
    cv2.imshow('Horizontal Stacking', hStack)
    #This is how we break out of the program
    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break

##  This is
cap.release()
cv2.destroyAllWindows()