class CameraHelper:
    def __init__(self, width, distance):
        self.width = width
        self.distance = distance
        self.focal_length = None

    def set_focal_length(self, marker):
        self.focal_length = (marker[1][0] * self.distance) / self.width

    def get_distance(self, pwidth):
        return (self.width * focalLength) / pwidth

        
