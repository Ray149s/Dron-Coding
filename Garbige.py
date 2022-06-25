# import cv2 
# import numpy
# print(cv2.__version__)
# print(numpy.__version__)


import ImageStacker
import cv2
import numpy as np
import os


# ######################################
# #Example of how to call and implement the ImageStacker class for picture
# ######################################
# img = cv2.imread('C:/Users/duena/OneDrive/Documents/Dron Coding/Prictice Files/LandingPadImgs/RayWedding.jpg')

# kernel = np.ones((5,5),np.uint8)
# ##These next 5 lines just change the filter that is being ablied to the image
# imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
# imgCanny = cv2.Canny(img,150,200)
# imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
# imgEroded = cv2.erode(imgDialation,kernel,iterations=1)


# StackWindow = ImageStacker.stackImages(0.5,([img, imgGray, imgBlur], [imgCanny, imgDialation, imgEroded]))
# cv2.imshow('Stacked immages', StackWindow)


 
# # cv2.imshow("Gray Image",imgGray)
# # cv2.imshow("Blur Image",imgBlur)
# # cv2.imshow("Canny Image",imgCanny)
# # cv2.imshow("Dialation Image",imgDialation)
# # cv2.imshow("Eroded Image",imgEroded)
# cv2.waitKey(0)

# ######################################
# #Example of how to call and implement the ImageStacker class for video feed
# ######################################

frameWidth = 640
frameHeight  = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    #cv2.imshow("Result", img)
    
    kernel = np.ones((5,5),np.uint8)
    print(kernel)

    ##These next 5 lines just change the filter that is being ablied to the image
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
    imgCanny = cv2.Canny(img,150,200)
    imgDialation = cv2.dilate(imgCanny,kernel,iterations=2)
    imgEroded = cv2.erode(imgDialation,kernel,iterations=2)
    imgBlank = np.zeros((200,200),np.uint8)


    StackWindow = ImageStacker.stackImages(0.8,([img, imgGray, imgBlur], [imgCanny, imgDialation, imgEroded]))
    cv2.imshow('Stacked immages', StackWindow)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




