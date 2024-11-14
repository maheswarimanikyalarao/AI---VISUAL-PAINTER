
import numpy as np
import cv2
import mediapipe as mp
import time
class handDetector( ):
    def __init__(self,  mode=False, maxhands=2,complexity=1, detectioncon=0.5, trackcon=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.complexity=complexity
        self.detectioncon=detectioncon
        self.trackcon=trackcon
        self.mpHands= mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxhands,self.complexity,self.detectioncon,self.trackcon)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipids=[4,8,12,16,20]





    def findhands(self, img ):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(self.imgRGB)
        if self.results.multi_hand_landmarks:

            for handlms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
                #for id,lm in enumerate(handlms.landmark):
        return img

    def findposition(self,img,handNo=0,draw=True):
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            handlms=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape


                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)

                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        return self.lmlist

    def fingersup(self):
        finger=[]
        if self.lmlist[self.tipids[0]][1]<self.lmlist[self.tipids[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)
        for id in range(1,5):
            if self.lmlist[self.tipids[id]][2]<self.lmlist[self.tipids[id]-2][2]:
                finger.append(1)
            else:
                finger.append(0)
        return finger



def main():


    cap = cv2.VideoCapture(0)
    detector=handDetector
    ptime = 0
    ctime = 0
    while True:
        success, img = cap.read()
        img = detector.findhands( img=img )
        # print(results)


        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)

        cv2.imshow("image", img)
        cv2.waitKey(1)
#if __name__ =="__main__":
    #main()


