from facial_detection import ImageDetection
import cv2

camera = cv2.VideoCapture(0)
detector = ImageDetection()

while 1:
    ret, img = camera.read()
    face = ImageDetection.detect_face(img)

    cv2.imshow('img', img)

    print(face)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector

