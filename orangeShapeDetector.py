import cv2 as cv
import numpy as np   

capture = cv.VideoCapture(0)

#set HSV range for orange colors
RGBorange = np.uint8([[[255, 103 ,0]]])
HSVOrange = cv.cvtColor(RGBorange, cv.COLOR_RGB2HSV)
lowerLimit = HSVOrange[0][0][0] - 10, 120, 120
lowerLimit = np.array(lowerLimit, dtype=np.uint8)
upperLimit = HSVOrange[0][0][0] + 5, 255, 255
upperLimit = np.array(upperLimit, dtype=np.uint8)

""" print(HSVOrange)
print(lowerLimit)
print(upperLimit) """

while True:
    isTrue, frame = capture.read()
    blank = np.zeros(frame.shape, dtype='uint8')
    
    blurFrame = cv.GaussianBlur(frame, (7,7), cv.BORDER_DEFAULT)
    hsvFrame = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV) 
    mask = cv.inRange(hsvFrame, lowerLimit, upperLimit) #filter out nonornge colors
    maskDilated = cv.dilate(mask, (5,5), iterations=5)
    #orangeFrame = cv.bitwise_and(frame, frame, mask=mask)  
      
    contours, hierarchy = cv.findContours(maskDilated, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) #for getting outline of orange shapes
    
    #if orange shape is big enough, draw an rectange over it
    for pic, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if(area > 6000):
            x, y, w, h = cv.boundingRect(contour)
            frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 103, 255), 2)
   
    #cv.imshow("hsv", hsvFrame)
    cv.imshow("maskDia", maskDilated)
    
    cv.drawContours(blank, contours, -1, (0,103,255), 2)
    cv.imshow('outline', blank)
    
    cv.imshow("Frame", frame)
    #cv.imshow("orangeDetect", orangeFrame)
    
    
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()

