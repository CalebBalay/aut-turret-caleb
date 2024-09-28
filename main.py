from facial_detection import ImageDetection
import cv2

camera = cv2.VideoCapture(0)
detector = ImageDetection()
dimensions = (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

while 1:
    ret, img = camera.read()
    face = ImageDetection.detect_face(detector, img)

    if len(face) > 0:
        (x, y, w, h) = face[0]
        cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)

    cv2.circle(img, (int(dimensions[0]/2), int(dimensions[1]/2)), int(dimensions[1]/2), (0, 255, 0), 2)
      
    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera.release()
del detector

