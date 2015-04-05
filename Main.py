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
import skindetection
# Script options
VIDEO_SOURCE = 0#\
#'/home/mehdi/vision/Sample-Video/Hand_PatternDrawing.avi'
#
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
	if frame_number < 2:
		frames_first3s.append(frame_input)
	elif frame_number == 2:
		frame_background = np.uint8(np.mean(frames_first3s, axis=0))
	# process from 3s
	else:
		crop_point, frame_output_1, frame_output_2 = \
             		background.remove_background(
			frame_background=frame_background, frame_input=frame_input)

		
		if crop_point[0]==-1 or crop_point[1]==-1 or \
			np.min([frame_output_1.shape[0], frame_output_1.shape[1]])<4:
			continue
		cv2.imshow('output video 1', frame_output_1)
		cv2.imshow('output video 2', frame_output_2)
		
		cv2.waitKey(int(1000*0.10/VIDEO_FR))

		# Start of Phase 2
		#frame_justSkin = skindetection.skin_detector(frame_output_1)
		frame_justSkin = skindetection.skin_detector(frame_output_1)
		#frame_justSkin = skindetection.skin_detector(frame_output_2)
		cv2.imshow('output video 3', frame_justSkin)
		cv2.waitKey(int(500*1.0/VIDEO_FR))

		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
