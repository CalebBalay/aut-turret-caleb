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

camera = cv2.VideoCapture(2)
detector = ImageDetection()

dimensions = (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

#ser = serial.Serial('COM9', 9600, timeout=.1)
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
            #ser.write('b'.encode())
    cv2.imshow('img', img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector