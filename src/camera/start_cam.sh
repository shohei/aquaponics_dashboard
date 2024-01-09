#!/usr/bin/sh
python camera_streaming/app.py &
python camera_contour/app.py &
python camera_optical_flow/app.py &
#python camera_facedetection/app.py
