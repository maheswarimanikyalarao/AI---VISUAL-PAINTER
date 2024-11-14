import mediapipe as mp
import cv2
import os
import numpy as np
import time
import handTracking_module as htm
brushthickness=15
eraserthickness=30
xp=0
yp=0

folderpath="projectimage"
mylist=os.listdir(folderpath)
#print(mylist)
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
#print(len(overlaylist))
header=overlaylist[0]

detector=htm.handDetector( )
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
drawcolor=(255,0,255)
imgcanvas=np.zeros((720,1280,3),np.uint8)
while True:
    #import image
    success, img=cap.read()
    img=cv2.flip(img,1)
    img[0:125, 0:1280] = header
    img=detector.findhands(img)

    lmlist=detector.findposition(img)


    if len(lmlist)!=0:
        #print(lmlist[8])


        #tip of index finger and middle finger
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        # 3.check which fingers are up
        fingers=detector.fingersup()
        #print(fingers)

        if fingers[1]and fingers[2]:
            #print('selection mode')
            xp=0
            yp=0
            if y1<125:
                if 220<x1<345:
                    header=overlaylist[0]
                    drawcolor=(255,0,255)
                elif 400<x1<550:
                    header=overlaylist[1]
                    drawcolor=(255,0,0)
                elif 640<x1<750:
                    drawcolor=(0,255,0)
                    header=overlaylist[2]
                elif 780<x1<900:
                    drawcolor=(0,0,0)
                    header=overlaylist[3]
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)
        if fingers[1] and fingers[2]== False:
            #print('drawing mode')
            cv2.circle(img, (x1, y1), 15, drawcolor, cv2.FILLED)
            if(xp==0 and yp==0):
                xp,yp=x1,y1





            if drawcolor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, eraserthickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, brushthickness)

        xp,yp=x1,y1
        imgGray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
        _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
        imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img=cv2.bitwise_and(img,imgInv)
        img=cv2.bitwise_or(img,imgcanvas)

    #2.ffind handlandmarks


    #4.if two fingers are up selection mode
    #5.if one finger up drawing mode
    # setting the header image

    #img=cv2.addWeighted(img,0.5,imgcanvas,0.5,0)

    cv2.imshow("image", imgcanvas)
    cv2.imshow("image", img)

    cv2.waitKey(1)