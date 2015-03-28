"""
This is the main module of the gesture_authenticator project
"""
# Imports
import pdb
import time

import numpy as np
import matplotlib.pyplot as plt
import cv2

import background
# Script options
VIDEO_SOURCE = \
    '/mnt/Data/Documents/Courses/SmartEnvironmentVision/Hand_PatternDrawing.avi'
VIDEO_FR = 30.0
# Script starts here
video_capture = cv2.VideoCapture(VIDEO_SOURCE)
frame_number = 0

frames_first3s = []

while video_capture.isOpened():
    # read from capture and display it
    frame_number += 1
    frame_time = frame_number / VIDEO_FR
    print('frame number: '+ str(frame_number))
    print('frame time: '+ str(frame_time))
    ret, frame_input = video_capture.read()
    cv2.imshow('input video', frame_input)
    # store first 3s frames
    if frame_time < 3:
        frames_first3s.append(frame_input)
    # process from 3s
    else:
        frame_output_1 = background.remove_background(
            frames_background=frames_first3s, frame_input=frame_input)

        cv2.imshow('output video', frame_output_1)
        cv2.waitKey(int(1000*1.0/VIDEO_FR))



