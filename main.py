from facial_detection import ImageDetection
import cv2
import time
from math import *


def get_difference(width, height, ex, ey):
    return sqrt((ex - width / 2) ** 2 + (ey - height / 2) ** 2)
def get_angle(width, height, ex, ey):
    sine = abs(ey - height / 2) / get_difference(width, height, ex, ey)
    return asin(sine) + pi if x < width / 2 and y > height / 2 else \
            -asin(sine) + pi if x < width / 2 else \
                -asin(sine) + 2 * pi if y > height / 2 else asin(sine)

camera = cv2.VideoCapture(0)
detector = ImageDetection()
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

while 1:
    ret, img = camera.read()
    face = ImageDetection.detect_face(detector, img)
    
    for (x,y,w,h) in face:
        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    cv2.rectangle(img, (int(width / 2), int(height / 2)), (int(width / 2 + 10), \
                  int(height / 2 + 10)),\
                  (255,255,0),2) 
    if len(face) != 0:
        print(face)
        print(f"distance is {get_difference(width, height, face[0][0], face[0][1])}")
        print(f"angle is {get_angle(width, height, face[0][0], face[0][1])}")
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector

