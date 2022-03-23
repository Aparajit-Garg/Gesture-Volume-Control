import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm
import osascript

# result = osascript.osascript('get volume settings')
# print(result)

minVol = 0
maxVol = 100

###### DEFINING CAM PROPERTIES
wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionConf=0.7)

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    points = detector.findPosition(img, draw=False)

    if len(points) != 0:
        x1, y1 = points[4][1], points[4][2]
        x2, y2 = points[8][1], points[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        print(x1, y1)

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        length = math.hypot(x2 - x1, y2 - y1)

        # vol = np.interp(length, [50, 300], [minVol, maxVol])
        # osascript.osascript("set volume output volume {}".format(vol))
        # result = osascript.osascript('get volume settings')
        # print(result)
        # print("\n\n")
        # print(length)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
