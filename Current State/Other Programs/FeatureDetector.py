import cv2
import numpy as np
import os
#add in ,0 imports the images in grey scale
img1 = cv2.imread('C:/Users/duena/OneDrive/Documents/Dron Coding/Prictice Files/LandingPadImgs/RayWedding.jpg')
#img2 = cv2.imread('',0)
img2 = cv2.imread('C:/Users/duena/OneDrive/Documents/Dron Coding/Resources/Images/LandingPadImgs/RayWedding.jpg')
img1= cv2.resize(img1,(500,600))
img2= cv2.resize(img2,(500,600))

# What is this doing ORB detecture uses fetures it contains to describe fetures in the image you feed it.  It can use 500 descripters per mages
# we can increas and decrease the number of features that it needs to find default is 500 fetures but we could fright 100
orb = cv2.ORB_create(nfeatures=800)

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

imgKp1 = cv2.drawKeypoints(img1,kp1,None)
imgKp2 = cv2.drawKeypoints(img2,kp2,None)



# our braut force mathcer
bf = cv2.BFMatcher()
# knnMatch takes descritpter 1 and descripter 2 and the K value which gives us 2 values to compare, and gives us all the matches that it can find. 
matches = bf.knnMatch(des1,des2,k=2)

# we can look at our matches and determin if they are good or bad
good=[]
for m,n in matches:
    # Whenever the distance between the values we get our low we will say it is a good match when the values between are high then we will say its a bad match. 
    # depending on results we can adjust the .75 number
    if m.distance < 0.75*n.distance:
        good.append([m])
print(len(good))

# We can plot out our matches to see what we are getting
# good meanns good matches will be sown, None refers to the out image, flag is how do we want to show and wi write that we want to show in format 2
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)


cv2.imshow('Kp1', imgKp1)
cv2.imshow('Kp2', imgKp2)
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img2', img3)
cv2.waitKey(0)
