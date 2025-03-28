from facial_detection import ImageDetection
import cv2
import time
import serial
from math import *
from color_detection import ColorDetection
import os

def within_bounds(x, y, lowX, highX, lowY, highY):
    return (x >= lowX and x <= highX) and (y >= lowY and y <= highY)

def get_magnitude(width, height, ex, ey):
    return sqrt((ex - width / 2) ** 2 + (ey - height / 2) ** 2)

def get_angle(width, height, ex, ey):
    sine = abs(ey - height / 2) / get_magnitude(width, height, ex, ey)
    return asin(sine) + pi if x < width / 2 and y > height / 2 else \
            -asin(sine) + pi if x < width / 2 else \
                -asin(sine) + 2 * pi if y > height / 2 else asin(sine)

camera = cv2.VideoCapture(4)
detector = ImageDetection()
color = ColorDetection()
dimensions = (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

#ser = serial.Serial('COM9', 9600, timeout=.1)
xPixToRot = 180 / dimensions[0]
yPixToRot = 180 / dimensions[1]
turX = 105
turY = 103
rate = 5
buffer = 40
wait_time = 3
last_time = time.time()

ser = serial.Serial('COM9', 9600, timeout=.1)
while 1:
    ret, img = camera.read()
    face = ImageDetection.detect_face(detector, img)
    eyes = ImageDetection.detect_eyes(detector, img)

    (x,y,w,h) = (0,0,0,0)
    if len(eyes) > 0 and len(eyes) < 3: #and color.detect_orange(img):
        #(x, y, w, h) = face[0]
        #cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 2)
        if (len(eyes[0]) == 2):
            bfeye = eyes[0][0]
            (x, y, w, h) = bfeye
            cv2.line(img, (int(dimensions[0]/2), int(dimensions[1]/2)), \
                (x + int(w/2), y + int(h/2)), (0, 0, 0), 2)
            print(w, h)
            
            posx = x * xPixToRot
            posy = y * yPixToRot
            
            while 1:
                print(f"x:{turX}, y:{turY}")
                if x + w / 2 > dimensions[0] / 2 + buffer and turX <= 180 - rate\
                    and time.time() >= last_time + wait_time:
                    ser.write('b'.encode())
                    turX += rate
                    break
                elif x + w / 2 < dimensions[0] / 2 - buffer and turX >= rate\
                      and time.time() >= last_time + wait_time:
                    ser.write('a'.encode())
                    turX -= rate
                    break
                if (x + w / 2 >= dimensions[0] / 2  - buffer and\
                    x + w / 2 <= dimensions[0] / 2  + buffer) or (x >= 180 or x < rate):
                    if not (x >= 180 or x < rate):
                        last_time = time.time()
                    break
            while 1:
                if y + h / 2 > dimensions[1] / 2 + buffer and turY <= 180 - rate\
                    and time.time() >= last_time + wait_time:
                    ser.write('c'.encode())
                    turY += rate
                    break
                elif y + h / 2 < dimensions[1] / 2 - buffer and turY >= rate\
                    and time.time() >= last_time + wait_time:
                    ser.write('d'.encode())
                    turY -= rate
                    break
                if (y + h / 2 <= dimensions[1] / 2  + buffer and\
                    y + h / 2>= dimensions[1] / 2  - buffer) or (y >= 180 or y < rate):
                    if not (x >= 180 or x < rate):
                        last_time = time.time()
                    break
                print(f"x:{turX}, y:{turY}")
        #ser.write('b'.encode())
    cv2.imshow('img', img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector