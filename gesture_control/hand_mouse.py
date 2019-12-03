# This code works with python2.
# Please install opencv: conda install opencv
# Quartz: conda install -c conda-forge pyobjc-framework-quartz 

import cv2
import numpy as np
import pymouse

palm = cv2.CascadeClassifier('./haarcascades/palm.xml')
fist = cv2.CascadeClassifier('./haarcascades/fist.xml')
m = pymouse.PyMouse()

cap = cv2.VideoCapture(0)
while True:
    ret, img =cap.read()
    # flip_img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    palm_cascade = palm.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in palm_cascade:
        cv2.rectangle(img , (x,y) , ((x+w),(y+h)), (255,0,0), 2)
        m.move(int(x + w/2), int(y + h/2))
     
    fist_cascade = fist.detectMultiScale(gray,1.3,5)
    for(xf,yf,wf,hf) in fist_cascade:
        cv2.rectangle(img , (xf,yf) , ((xf+wf),(yf+hf)), (0,0,255), 2)
        # 1: left, 2: right, 3: middle
        m.click(int(xf + wf/2), int(yf + hf/2), 1)
        
    #cv2.namedWindow("img",cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('img',img)
     
    k = cv2.waitKey(30) & 0xff
    if k == 27: # 'esc'
        break      
    
cap.release()
cv2.destroyAllWindows() 
