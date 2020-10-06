import cv2
import numpy as np
import os

def nothing(x):
    pass

def calc_distance(knownWidth, focalLength, pixelWidth):
    return (knownWidth * focalLength) / pixelWidth


fileobj = None
name = None
PATH = "saves/"
pageNo = 1
LOW_HSV = None
HIGH_HSV = None
EROSION_ITR = None
DIALATION_ITR = None
hsvSaved = False
drawFlag = False
distanceFlag = False
focalLength = None
distance = 0
page = None
tool = "pen"
height = None
width = None
b, g, r = 255, 255, 255
penSize = 2
eraserRadius = 2

x1 = 0
y1 = 0

name = input("Enter name of file: ")

if (not os.path.isdir(PATH + name)):
    os.makedirs(PATH + name)
    fileobj = open(PATH + name + "/pgno.txt", "w+")
    print("file created")
else:
    fileobj = open(PATH + name + "/pgno.txt", "r+")
    pageNo = int(fileobj.read())
    fileobj.seek(0)
    fileobj.truncate()
    print("file exists")

knownDistance = float(input("Enter known Distance in cm : "))
knownWidth = float(input("Enter known Width of Object in cm : "))
threshDist = float(input("Enter Threshold in cm : "))

kernel = np.ones((5, 5), np.uint8)
print("press s to save image")
print("press d to start writing")
print("press q to quit")

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 300, 350)
cv2.createTrackbar("Low_Hue", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Low_Sat", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Low_Val", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Up_Hue", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Up_Sat", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Up_Val", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Erosion", "Trackbars", 0, 2, nothing)
cv2.createTrackbar("Dialation", "Trackbars", 0, 2, nothing)

cv2.namedWindow("Tool_Box")
cv2.resizeWindow("Tool_Box", 300, 350)
cv2.createTrackbar("blue", "Tool_Box", 0, 255, nothing)
cv2.createTrackbar("green", "Tool_Box", 0, 255, nothing)
cv2.createTrackbar("red", "Tool_Box", 255, 255, nothing)
cv2.createTrackbar("Pen_size", "Tool_Box", 2, 20, nothing)
cv2.createTrackbar("Eraser_size", "Tool_Box", 2, 20, nothing)

color = np.zeros((100, 350, 3), np.uint8)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if page is None:
        page = np.zeros_like(frame)

    height, width, dimension = frame.shape

    outputBg = np.zeros((200, width, 3), dtype=np.uint8)

    cv2.rectangle(page, (0, 10), (20, 30), [0, 0, 255], 2)
    cv2.rectangle(page, (0, 40), (20, 60), [0, 0, 255], 2)

    color[:] = [b, g, r]

    l_h = cv2.getTrackbarPos("Low_Hue", "Trackbars")
    l_s = cv2.getTrackbarPos("Low_Sat", "Trackbars")
    l_v = cv2.getTrackbarPos("Low_Val", "Trackbars")
    u_h = cv2.getTrackbarPos("Up_Hue", "Trackbars")
    u_s = cv2.getTrackbarPos("Up_Sat", "Trackbars")
    u_v = cv2.getTrackbarPos("Up_Val", "Trackbars")
    erosion_itr = cv2.getTrackbarPos("Erosion", "Trackbars")
    dialation_itr = cv2.getTrackbarPos("Dialation", "Trackbars")

    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    b = cv2.getTrackbarPos("blue", "Tool_Box")
    g = cv2.getTrackbarPos("green", "Tool_Box")
    r = cv2.getTrackbarPos("red", "Tool_Box")
    penSize = cv2.getTrackbarPos("Pen_size", "Tool_Box")
    eraserRadius = cv2.getTrackbarPos("Eraser_size", "Tool_Box")
    
    if (hsvSaved == False):
        mask = cv2.inRange(hsv_img, lower_range, upper_range)
        mask = cv2.erode(mask, kernel, iterations=erosion_itr)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=dialation_itr)
    else:
        mask = cv2.inRange(hsv_img, LOW_HSV, HIGH_HSV)
        mask = cv2.erode(mask, kernel, iterations=EROSION_ITR)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=DIALATION_ITR)

    masked_frame = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((mask_bgr, frame, masked_frame))

    contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contour and cv2.contourArea(max(contour, key=cv2.contourArea)) > 500:
        
        c = max(contour, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x + w, y + h), [b, g, r], 4)

        if distanceFlag == True:
            distance = calc_distance(knownWidth, focalLength, w)
            print("Distance of object is: ", distance)

        if (drawFlag == True and distance < threshDist):

            if tool == "pen":

                cv2.circle(frame, (x, y), penSize, [b, g, r], -1)

                if (x1 == 0 and y1 == 0):
                    x1, y1 = x, y

                else:
                    page = cv2.line(page, (x1, y1), (x, y), [b, g, r], penSize)
                    print("pen")
                    x1, y1 = x, y
            else:
                cv2.circle(frame, (x, y), eraserRadius, [0, 0, 0], -1)
                cv2.circle(page, (x, y), eraserRadius, [0, 0, 0], -1)
                x1, y1 = 0, 0
                print("Eraser")
    else:
        x1, y1 = 0, 0

    frame = cv2.add(frame, page)
    if (drawFlag == False):
        cv2.imshow("Find_Hsv", cv2.resize(stacked, None, fx=0.2, fy=0.4))
    else:
        cv2.imshow("page", page)
        mon = frame.copy()
        cv2.putText(outputBg, "tool: " + tool, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255,0), 1)
        if (distanceFlag == True):
            cv2.putText(outputBg, "distance : {:.2f}".format(distance), (5, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 255,0), 1)

        if (drawFlag==True and distance>=threshDist):
            cv2.putText(outputBg, "Distance exceeded Threshold Distance", (5, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (0, 255,0), 1)

        show = np.vstack((mon, outputBg))

        cv2.imshow("frame", cv2.resize(show, None, fx=0.6, fy=0.6))
        cv2.imshow("Tool_Box", color)

    key = cv2.waitKey(1) & 0xFF

    if (key == ord('d') and drawFlag == False):
        LOW_HSV = lower_range
        HIGH_HSV = upper_range
        EROSION_ITR = erosion_itr
        DIALATION_ITR = dialation_itr
        cv2.destroyWindow("Trackbars")
        cv2.destroyWindow("Find_Hsv")
        hsvSaved = True
        drawFlag = True

    if key == ord('e') or (x < 20 and y < 30 and y > 10):
        if tool == "pen":
            tool = "eraser"
        else:
            tool = "pen"
        continue

    if key == ord('c') or (x < 40 and y < 60 and y > 40):
        page = None
        continue

    if (key == ord('m')):
        focalLength = (w * knownDistance) / knownWidth
        distanceFlag = True

    if (key == ord('s')):
        cv2.imwrite(PATH + name + "/" + str(pageNo) + ".jpg", page)
        pageNo += 1
        print("Saved")

    if (key == ord('q')):
        fileobj.write(str(pageNo))
        fileobj.close()
        break

cv2.destroyAllWindows()
cap.release()
