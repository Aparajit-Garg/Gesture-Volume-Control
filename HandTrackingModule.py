import cv2
import mediapipe as mp
import time

class handDetector():
    # the arguments are required by mediapipe library functions
    def __init__(self, mode= False, maxHands=2, detectionConf= 0.5, trackConf= 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x) * w, int(lm.y) * h
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 720)
    cap.set(4, 1280)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        points = detector.findPosition(img)
        if len(points) != 0:
            print(points[4])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        # cv2.putText()
        cv2.imshow("img", img)
        cv2.waitKey(1)

# main()