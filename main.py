from facial_detection import ImageDetection
import cv2
import time
import serial
from math import *

def get_magnitude(width, height, ex, ey):
    return sqrt((ex - width / 2) ** 2 + (ey - height / 2) ** 2)

def get_angle(width, height, ex, ey):
    sine = abs(ey - height / 2) / get_magnitude(width, height, ex, ey)
    return asin(sine) + pi if x < width / 2 and y > height / 2 else \
            -asin(sine) + pi if x < width / 2 else \
                -asin(sine) + 2 * pi if y > height / 2 else asin(sine)

camera = cv2.VideoCapture(0)
detector = ImageDetection()

dimensions = (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

ser = serial.Serial('COM9', 9600, timeout=.1)
xMinAbs = 0
yMinAbs = 0
xMinAbs = 180
yMinAbs = 180
xMinCam = 30
yMinCam = 95
xMaxCam = 120
yMaxCam = 135
turX = (xMaxCam - xMinCam) / 2 + xMinCam
turY = (yMaxCam - yMinCam) / 2 + yMinCam
rate = 5
buffer = 20

while 1:
    ret, img = camera.read()
    face = ImageDetection.detect_face(detector, img)
    eyes = ImageDetection.detect_eyes(detector, img)

    (x,y,w,h) = (0,0,0,0)
    if len(face) == 1:
        (x, y, w, h) = face[0]

        if len(eyes) > 0:
            (x, y, w, h) = eyes[0]
            cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 2)
            
            theta = get_angle(int(dimensions[0]), int(dimensions[1]), x, y)
            mag = get_magnitude(int(dimensions[0]), int(dimensions[1]), x, y)
    
            cv2.line(img, (int(dimensions[0]/2), int(dimensions[1]/2)), \
                      (int(mag*cos(theta) + int(dimensions[0]/2)), \
                      -int(mag*sin(theta)) + int(dimensions[1]/2)), (0, 0, 0), 2)
            ratx = x / dimensions[0]
            raty = y / dimensions[1]
            difx = xMaxCam - xMinCam
            dify = yMaxCam - yMinCam
            while 1:
                print(f"x:{turX}, y:{turY}")
                if turX < ratx * difx + xMinCam:
                    ser.write('b'.encode())
                    turX += rate
                elif turX > ratx * difx + xMinCam:
                    ser.write('a'.encode())
                    turX -= rate
                if turX >= ratx * difx + xMinCam - buffer and\
                    turX <= ratx * difx + xMinCam + buffer:
                    break
            while 1:
                if turY < raty * dify + yMinCam:
                    ser.write('c'.encode())
                    turY += rate
                elif turY > raty * dify + yMinCam:
                    ser.write('d'.encode())
                    turY -= rate
                if turY >= raty * dify + yMinCam - buffer and\
                    turY <= raty * dify + yMinCam + buffer:
                        break
                print(f"x:{turX}, y:{turY}")
                
    cv2.imshow('img', img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector