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

    	#cv2.imshow('HSV video', frame_HSV)

	# tresholding for find skin
	#height, width = frame_HSV.shape[:2]
	#frame_skin_detected = np.zeros((height, width, 3), np.uint8)

	low_range1 = np.array([0, 60, 70], dtype="uint8")
	high_range1 = np.array([20, 255, 255], dtype="uint8")
	low_range2 = np.array([150, 60, 70], dtype="uint8")
	high_range2 = np.array([200, 255, 255], dtype="uint8")

	skin_detected_1 = cv2.inRange(frame_HSV, low_range1, high_range1)
	skin_detected_2 = cv2.inRange(frame_HSV, low_range2, high_range2)
	skin_detected = cv2.bitwise_or(skin_detected_1, skin_detected_2)	

	kernel_h = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 2))
	kernel_v = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 6))
	
	skin_detected = cv2.erode(skin_detected, kernel_h, iterations=1)
	skin_detected = cv2.dilate(skin_detected, kernel_v, iterations=2)
	
	skin_detected = cv2.GaussianBlur(skin_detected, (3, 3), 0)
	skin_detected = 255 * (np.uint8(skin_detected/150))

	#cv2.imshow('Test', skin_detected)

	frame_BGR_skin = cv2.bitwise_and(frame_BGR_input, frame_BGR_input, mask=skin_detected)	
	
	
	return frame_BGR_skin

