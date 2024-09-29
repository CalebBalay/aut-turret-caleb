import cv2
import numpy as np

class ColorDetection:
    def __init__(self):
        self.orgr = np.uint8([[[255, 103, 0]]])
        self.orgh = cv2.cvtColor(self.orgr, cv2.COLOR_RGB2HSV)
        
        self.lbound = self.orgh[0][0][0] - 10, 120, 120
        self.lbound = np.array(self.lbound, dtype=np.uint8)
        
        self.ubound = self.orgh[0][0][0] + 5, 255, 255
        self.ubound = np.array(self.ubound, dtype=np.uint8)

    def get_contours(self, img):
        if img is not None:
            blank = np.zeros(img.shape, dtype='uint8')
            
            filtered = cv2.GaussianBlur(img, (7,7), cv2.BORDER_DEFAULT)
            filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
            filtered = cv2.inRange(filtered, self.lbound, self.ubound)
            filtered = cv2.dilate(filtered, (5,5), iterations=5)

            contours, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            return contours
        return None

    def is_significant_area(self, area):
        if (area > 6000):
            return True
        return False
    
    def find_first_contour(self, contours):
        if contours is not None:
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
            
                if self.is_significant_area(area):
                    return True
        return False

    def detect_orange(self, img):
        return self.find_first_contour(self.get_contours(img))

