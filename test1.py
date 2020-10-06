import cv2

cap = cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    #no_mirror=cv2.flip(frame,1)
    cv2.imshow("WINDOW",frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()