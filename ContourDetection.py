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
deadZone=100
global imgContour

## Defining function empty that will just pass because we dont want anything happening based on the trackbars
def empty(a):
    pass

## Defining window size resizing window size for track bars
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
## You will change the values of the thresh hold once you use the track bar to determen the best values for these perramiters
cv2.createTrackbar("Threshold1", "Parameters",150,255,empty)
cv2.createTrackbar("Threshold2", "Parameters",255,255,empty)
cv2.createTrackbar("Area", "Parameters",5000,30000,empty)


## Makeing a funcion to get the contors of our image
def getContours(img,imgContour):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    ## To address the nois in our contour detection we will use a min area in order to quolify their display
    for cnt in contours:
        area = cv2.contourArea(cnt)
        ## Settting area minim to the value set in our track bar
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area>areaMin:
            ## (imgContour comes from getContour peramiters, contours comes from line above, -1 is , (xxx,xxx,xxx), -7 is the width of the boundary)
            cv2.drawContours(imgContour, contours, -1, (255, 0, 255), 7)

## Now we adress the CORNER DETECTION to do so we need to know the length of our contors 
            ## True implies theat the contour is closed
            peri = cv2.arcLength(cnt, True)
            ## opproximates the shape of the contour and again True impliese closed
            ## It accepts the contour cnt, resolution 0.2 * peri, and T/F valuse as peramiters 
            ## based on the number of points that show up in this given array we can determin the shape we have in the frame
            approx = cv2.approxPolyDP(cnt, 0.2 * peri, True)
            ##P Printing out the nuber of corner points that have been found in the image
            print(len(approx))
## Now we make a ounding Box
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            ## Here we add text to the contours of our image in the first line we add the number of points detected then in the second line we add the area of the enclosed contour 
            ##(the contour of focus, string to print next to contoru, initial location, font, skale, color and thickness)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7, (0.255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7, (0.255, 0), 2)
            cv2.putText(imgContour, " " + str(int(x)) + " " + str(int(y)), (x - 20, y -45), cv2.FONT_HERSHEY_COMPLEX, .7, (0.255, 0), 2)
            
            cx = int(x + (w / 2))
            cy = int(y + (h / 2))
 
            if (cx <int(frameWidth/2)-deadZone):
                cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            elif (cx > int(frameWidth / 2) + deadZone):
                cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
            elif (cy < int(frameHeight / 2) - deadZone):
                cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
            elif (cy > int(frameHeight / 2) + deadZone):
                cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
 
 
            cv2.line(imgContour, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),
                     (0, 0, 255), 3)


def display(img):
    cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)
 
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)
 




## Iterates and gives s the outut of each frame that is stored in img varaible 
while True:
    ## calling the feed for image frames
    success, img = cap.read()
    imgContour = img.copy()
    ## Gaussian Blur function with a kurnal of 7x7 converting image into a more blured version
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)

    ## now we convert our blurd image into gray skale
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    ## Grabing the valuse in the track bars
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    ## these next lines will help with the overlap seen on the contors of our immage 
    imgCanny = cv2.Canny(imgGray, threshold1,threshold2)   
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    
    getContours(imgDil,imgContour)
  
    
    ## Displaying the stacked windows in one window
    imgStack = IS.stackImages(0.8, ([img, imgBlur, imgGray], [imgContour, imgContour, imgDil]))

    cv2.imshow("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break