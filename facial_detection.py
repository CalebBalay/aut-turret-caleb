import cv2

# cv2 wrapper
class ImageDetection:
    def __init__(self):
        self.img = None
        self.fcs = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.ecs = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.faces = None

    def __del__(self):
        cv2.destroyAllWindows()

    def detect_face(self, img):
        if img is not None:
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return self.fcs.detectMultiScale(img_grey, 1.3, 5)
        return None
    def detect_eyes(self, img):
        if img is not None:
            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return self.ecs.detectMultiScale(img_grey)
        return None
    



