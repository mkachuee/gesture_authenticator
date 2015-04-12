"""
This module implements part1 of phase2 of the project
"""
# imports
import pdb
import numpy as np
import cv2

# options
def skin_detector(frame_BGR_input, face_rectangles):
	"""
	This function converts input frame to HSV and detects area of skin
	"""
	#int i=0
	#for (x, y, w, h) in face_rectangle :
	#	face_BGR[i] = frame_BGR_input[y:y+h, x:x+w]
	#	i+=1
	#
	# convert to HSV space
	frame_HSV = cv2.cvtColor(frame_BGR_input, cv2.COLOR_BGR2HSV)
	#face_HSV = cv2.cvtColor(face_BGR[0], cv2.COLOR_BGR2GRAY)
    	cv2.imshow('HSV video', frame_HSV)
	# tresholding for find skin
	#height, width = frame_HSV.shape[:2]
	#frame_skin_detected = np.zeros((height, width, 3), np.uint8)
	low_range = np.array([0, 60, 70], dtype="uint8")
	high_range = np.array([20, 255, 255], dtype="uint8")
	skin_detected0 = cv2.inRange(frame_HSV, low_range, high_range)
	
	kernel_v = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
	kernel_h = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 1))

	skin_detected2 = cv2.erode(skin_detected0, kernel_h, iterations=1)
	skin_detected2 = cv2.dilate(skin_detected2, kernel_v, iterations=1)
	
	
	cv2.imshow('Test', skin_detected2)

	#skin_detected = cv2.erode(skin_detected, kernel, iterations=1)
	#skin_detected1 = cv2.dilate(skin_detected0, kernel_v, iterations=2)

	#skin_detected1 = cv2.GaussianBlur(skin_detected1, (3, 3), 0)
	skin_detected2 = cv2.GaussianBlur(skin_detected2, (3, 3), 0)

	frame_BGR_skin = cv2.bitwise_and(frame_BGR_input, frame_BGR_input, mask=skin_detected2)	
	
	#cv2.imshow('skin binary', frame_skin_detected)
	#frame_BGR_skin = np.tile(frame_skin_detected.transpose()/255, (3, 1, 1)).transpose() * frame_BGR_input
	#cv2.imshow('skin detected in BGR', frame_BGR_skin)
	
	return frame_BGR_skin

