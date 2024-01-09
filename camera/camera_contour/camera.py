import cv2
from base_camera import BaseCamera
import sys
import time
import urllib.request
from influxdb import InfluxDBClient
import numpy as np
from datetime import datetime

def reduce_percent(scale_percent, img):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return dim

class Camera(BaseCamera):
    def __init__(self):
        super().__init__()

    @staticmethod
    def frames():
        dbclient = InfluxDBClient(host='localhost', port=8086, database='aquaponicsDB')

        url = "http://localhost:5000/video_feed"

        camera = cv2.VideoCapture(url)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        threshold = 141
        pix = 4

        while True:
               # read current frame
               _, img = camera.read()
               img_color = img.copy()
               img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
               #第一引数で指定したオブジェクトgrayscale_imgを輝度で平均化処理する。第二引数は平均化するピクセル数で、今回の場合は9,9は9x9ピクセルの計81ピクセル。
               img_blur = cv2.blur(img_gray,(pix,pix))
               #オブジェクトimg_blurを閾値threshold = 100で二値化しimg_binaryに代入
               ret, img_binary = cv2.threshold(img_blur, threshold, 255, cv2.THRESH_BINARY)
               #二値化した画像オブジェクトimg_binaryに存在する輪郭を抽出
               contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
               #抽出した輪郭の情報を用いて、オブジェクトimg_colorに書き出す
               img_color_with_contours = cv2.drawContours(img_color, contours, -1, (0,255,0), 2)
 
               # encode as a jpeg image and return it
               yield cv2.imencode('.jpg', img_color_with_contours)[1].tobytes()

