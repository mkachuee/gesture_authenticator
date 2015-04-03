"""
This module implements part1 of phase2 of the project
"""
# imports
import pdb
import numpy as np
import cv2

# options
def skin_detector(frame_BGR_input):
  	"""
  	This function converts input frame to HSV and detects area of skin
  	"""
  	# convert to HSV space
  	frame_HSV = cv2.cvtColor(frame_BGR_input, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV video', frame_HSV)
  	# tresholding for find skin
  	#height, width = frame_HSV.shape[:2]
  	#frame_skin_detected = np.zeros((height, width, 3), np.uint8)
  	frame_skin_detected = cv2.inRange(frame_HSV, (0, 70, 60), (20, 160, 255))
  	#cv2.imshow('skin binary', frame_skin_detected)
  	frame_BGR_skin = np.tile(frame_skin_detected.transpose()/255, (3, 1, 1)).transpose() * frame_BGR_input
  	#cv2.imshow('skin detected in BGR', frame_BGR_skin)
  	
  	return frame_BGR_skin
