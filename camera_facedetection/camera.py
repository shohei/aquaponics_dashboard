import cv2
from base_camera import BaseCamera
import sys
import time
import urllib.request

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
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        url = "http://192.168.1.221:5000/video_feed"

        camera = cv2.VideoCapture(url)
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

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

