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

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
class Camera2(BaseCamera):
    def __init__(self):
        super().__init__()
        print("cam2 init")

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        print("cam2 frames() triggered")
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
 
            dim = reduce_percent(60, img)
            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            #print("cam2 img:",id(img))
            # encode as a jpeg image and return it
            #yield cv2.imencode('.jpg', img)[1].tobytes()
            #print("yield gray: 2")
            yield cv2.imencode('.jpg', gray)[1].tobytes()

