import cv2
import matplotlib.pyplot as plt
import numpy as np

img= cv2.imread("./img/color_balls_1.jpeg")
plt.imshow(img)
plt.show(block="True")

#manual Try
#### convert to hsv
img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# low_red=np.array([0,0,0])
# high_red=np.array([0,0,255])
#
# plt.imshow(high_red)
# plt.show(block="True")
#
# cmask = cv2.inRange(img_hsv,low_red,high_red)
#
# new= cv2.bitwise_and(img,img,mask=cmask)
img[:,:,0]=0
print(img)
plt.imshow(img)
plt.show(block="True")


