from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from transform import four_point_transform

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
sensitivity = 15
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255,sensitivity,255])

pts = deque(maxlen=100)

COOR = []

vs = VideoStream(src=0).start()
time.sleep(2.0)


flag = False

coor_center = 0
coor_radius = False
while True:
    frame = vs.read()
    if frame is None:
        break

    frame = imutils.resize(frame, width=750)
    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", hsv)
    # cv2.imshow("blurred"wsdgjs d, blurred)

    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow("inRange", mask)
    mask = cv2.erode(mask, None, iterations=2)
    cv2.imshow("erode", mask)

    mask = cv2.dilate(mask, None, iterations=2)
    # cv2.imshow("dilate", mask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None



    for i in COOR:
        cv2.circle(frame, i, 8,(255, 0, 255), -1)

    if len(cnts) > 0:

        flag = True

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        coor_center = center
        coor_radius = radius
        # cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2 ) 


        # if len(COOR) <= 3 and radius > 15 : 
        #     print(COOR ,center)
        #     if not COOR:
        #         COOR.append(center) 
        #         print(COOR[-1][0] - center[0] , COOR[-1][1] - center[1] )

        #     if COOR and abs(COOR[-1][0] - center[0]) > 15 and abs(COOR[-1][1] - center[1])  > 15:
        #         COOR.append(center) 

        #     # input('ok ? ')

        if  radius > 0.2:
            
            pts.appendleft(center)
            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

            cv2.putText(frame ,str(radius).split('.')[0] ,center ,5 ,fontScale=2 , color=(0,255,255) )
            cv2.circle(frame, (int(x), int(y)), 1,(0, 0, 255), -1)
            cv2.circle(frame, (int(x), int(y)), int(radius+5),(255, 0, 0), 2)

            # cv2.circle(frame, center, 5, (0, 0, 255), -1)

    elif len(cnts) <= 0 :
        # pts = deque(maxlen=500)
            

        if len(COOR) <= 3 and flag and coor_radius: 
            flag = True
            # flag = False # NOTE : its later be correct!!

            if not COOR:
                COOR.append(coor_center) 

            if COOR and abs(COOR[-1][0] - coor_center[0]) > 15 and abs(COOR[-1][1] - coor_center[1])  > 15:
                COOR.append(coor_center) 

            cv2.circle(frame, (int(x), int(y)), int(coor_radius+5),(255, 0, 0), -1)


    # if len(COOR) == 4:
    #     frame = four_point_transform(frame , np.array([list(COOR[0]) ,list(COOR[1]) ,list(COOR[2]) ,list(COOR[3])]) )
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
    	break


vs.stop()
cv2.destroyAllWindows()