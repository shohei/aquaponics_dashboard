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

        # params for ShiTomasi corner detection
        feature_params = dict( maxCorners = 100,
                               qualityLevel = 0.3,
                               minDistance = 7,
                               blockSize = 7 )
        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        color = np.random.randint(0,255,(100,3))
        
        _, init_frame = camera.read()
        #init_frame = my_read(url)

        #dim = reduce_percent(60, init_frame)
        #init_frame = cv2.resize(init_frame, dim, interpolation = cv2.INTER_AREA)
        hsv = np.zeros_like(init_frame)
        hsv[...,1] = 255

        prev_time = time.monotonic()

        while True:
            # read current frame
            #img = my_read(url)
            _, img = camera.read()
 
            #dim = reduce_percent(60, img)
            #img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            prvs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #frame2 = my_read(url)
            _, frame2 = camera.read()
            #frame2 = cv2.resize(frame2 , dim, interpolation = cv2.INTER_AREA)
            next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            hsv[...,0] = ang*180/np.pi/2
            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            img_optical_flow = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

            average_flow = np.mean(mag)

            cur_time = time.monotonic()
            elapsed_time = cur_time - prev_time
            if(elapsed_time>5):
                # データベースへの書き込み
                json_body = [
                    {
                        "measurement": "aquaponics_measurement",
                        "time": datetime.utcnow(),
                        "fields": {
                            "average_flow": average_flow
                        }
                    }
                ]
                dbclient.write_points(json_body)
                #print('write average flow', average_flow)
                prev_time = cur_time 

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img_optical_flow)[1].tobytes()

