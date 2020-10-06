
## libraries
import cv2
import matplotlib.pyplot as plt
import  numpy as np
from skimage.filters import threshold_otsu

#########   Variable space
##########  For creating trackbars

def nothing(x):
    pass

## This flag becomes true whenmask detection is complete and we want to start writing
flag=False
## x1 and y1 stores previous co-ordinates of points since initially there will be no
x1,y1=0,0
## previous mask we make it zero
page=None
## 5 x 5 kernel used for erosion and dialation (dealing with noise)
kernel=np.ones((5,5),np.uint8)

## this  Trackbars are used to select mask by selecting proper range of HSV and nNUM of iterations to reduce noise
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",300,350)
cv2.createTrackbar("Low_Hue", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Low_Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Low_Val", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Up_Hue", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Up_Sat", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Up_Val", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Erosion", "Trackbars", 0,2,  nothing)
cv2.createTrackbar("Dialation","Trackbars",0,2,nothing)

## Video Capture Source (add fun of ip webcam)
cap=cv2.VideoCapture(0)

while True:

    ## Reading each frame from video
    ret,frame=cap.read()
    ## Flip the frame if source is web came (give it as a option to user)
    frame=cv2.flip(frame,1)

    ## if writing page is NOne make it black or white.
    if page is None:
        page=np.zeros_like(frame)

    ## Convert frame to HSV so that mask can be found easily
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ## Getting Mask Value from Trackbars(reading values)
    l_h = cv2.getTrackbarPos("Low_Hue", "Trackbars")
    l_s = cv2.getTrackbarPos("Low_Sat", "Trackbars")
    l_v = cv2.getTrackbarPos("Low_Val", "Trackbars")
    u_h = cv2.getTrackbarPos("Up_Hue", "Trackbars")
    u_s = cv2.getTrackbarPos("Up_Sat", "Trackbars")
    u_v = cv2.getTrackbarPos("Up_Val", "Trackbars")
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    ## Finding mask between Lower HSv and High Hsv
    mask = cv2.inRange(hsv_img, lower_range, upper_range)

    ## Applying Noise Reduction
    erosion_itr=cv2.getTrackbarPos("Erosion","Trackbars")
    dialation_itr = cv2.getTrackbarPos("Dialation", "Trackbars")
    mask = cv2.erode(mask, kernel, iterations=erosion_itr)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask = cv2.dilate(mask, kernel, iterations=dialation_itr)
    ## NOise Threshold used Static now
    thresh = 800

    masked_frame = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((mask_bgr, frame, masked_frame))

    if(flag==False):
        cv2.imshow("Find Mask", cv2.resize(stacked, None, fx=0.2, fy=0.4))
    if(cv2.waitKey(1) & 0xFF == ord('d')):
        cv2.destroyWindow("Find Mask")
        flag=True
    if(flag==True):
        contour,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if contour and cv2.contourArea(max(contour,key=cv2.contourArea))>100:
            c=max(contour,key=cv2.contourArea)
            x2,y2,w,h=cv2.boundingRect(c)
            print(x2,y2,w,h)
           # cv2.rectangle(frame,(x,y),(x+w,y+h),(50,60,70),10)
            if(x1==0 and y1==0):
                x1,y1=x2,y2
            else:
                page=cv2.line(page,(x1,y1),(x2,y2),[255,0,0],4)
                print("line")
            x1, y1 = x2, y2
            if(x2<60 and y2>406):
                page=None
                continue

        else:
            x1,y1=0,0




    frame=cv2.add(frame,page)
    cv2.imshow("frame",frame)
    cv2.imshow("page", page)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
