import cv2
from base_camera import BaseCamera
import sys
import time

def reduce_percent(scale_percent, img):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return dim

class Camera(BaseCamera):
    def __init__(self):
        super().__init__()
        print("cam1 init")

    @staticmethod
    def frames():
        print("cam1 frames() triggered")
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
 
            dim = reduce_percent(60, img)
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

