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

	low_range1 = np.array([0, 60, 70], dtype="uint8")
	high_range1 = np.array([9, 255, 255], dtype="uint8")
	low_range2 = np.array([170, 60, 70], dtype="uint8")
	high_range2 = np.array([180, 255, 255], dtype="uint8")

	skin_detected_1 = cv2.inRange(frame_HSV, low_range1, high_range1)
	skin_detected_2 = cv2.inRange(frame_HSV, low_range2, high_range2)
	skin_detected = cv2.bitwise_or(skin_detected_1, skin_detected_2)	

	kernel_h = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 2))
	kernel_v = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 6))
	
	skin_detected = cv2.erode(skin_detected, kernel_h, iterations=1)
	skin_detected = cv2.dilate(skin_detected, kernel_v, iterations=2)
	
	skin_detected = cv2.GaussianBlur(skin_detected, (3, 3), 0)
	skin_detected = 255 * (np.uint8(skin_detected/150))

	cv2.imshow('Test', skin_detected)

	frame_BGR_skin = cv2.bitwise_and(frame_BGR_input, frame_BGR_input, mask=skin_detected)	
	
	
	return frame_BGR_skin

def skin_detector2(frame_input, frame_BGS_input, face_rectangles):
	"""
	This function converts input frame to HSV and detects area of skin
	"""
	#int i=0
	#for (x, y, w, h) in face_rectangle :
	#	face_BGR[i] = frame_BGR_input[y:y+h, x:x+w]
	#	i+=1
	#
	# convert to HSV space
	frame_BGS_HSV = cv2.cvtColor(frame_BGS_input, cv2.COLOR_BGR2HSV)
	frame_HSV = cv2.cvtColor(frame_input, cv2.COLOR_BGR2HSV)
	#face_HSV = cv2.cvtColor(face_BGR[0], cv2.COLOR_BGR2GRAY)

	#cv2.imshow('HSV video', frame_HSV)

	# tresholding for find skin
	#height, width = frame_HSV.shape[:2]
	#frame_skin_detected = np.zeros((height, width, 3), np.uint8)

	low_range1 = np.array([0, 35, 70], dtype="uint8")
	high_range1 = np.array([20, 255, 255], dtype="uint8")
	low_range2 = np.array([160, 35, 70], dtype="uint8")
	high_range2 = np.array([180, 255, 255], dtype="uint8")

	low_range11 = np.array([0, 40, 70], dtype="uint8")
	high_range11 = np.array([10, 255, 255], dtype="uint8")
	low_range12 = np.array([170, 40, 70], dtype="uint8")
	high_range12 = np.array([180, 255, 255], dtype="uint8")

	skin_detected_1 = cv2.inRange(frame_BGS_HSV, low_range1, high_range1)
	skin_detected_2 = cv2.inRange(frame_BGS_HSV, low_range2, high_range2)
	skin_detected = cv2.bitwise_or(skin_detected_1, skin_detected_2)	

	skin_detected_01 = cv2.inRange(frame_HSV, low_range11, high_range11)
	skin_detected_02 = cv2.inRange(frame_HSV, low_range12, high_range12)
	skin_detected0 = cv2.bitwise_or(skin_detected_01, skin_detected_02)	

	kernel_h = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 2))
	kernel_v = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 6))
	
	skin_detected = cv2.erode(skin_detected, kernel_h, iterations=1)
	skin_detected = cv2.dilate(skin_detected, kernel_v, iterations=2)
	
	skin_detected0 = cv2.erode(skin_detected0, kernel_h, iterations=1)
	skin_detected0 = cv2.dilate(skin_detected0, kernel_v, iterations=2)
	
	skin_detected = cv2.GaussianBlur(skin_detected, (3, 3), 0)
	skin_detected = 255 * (np.uint8(skin_detected/150))

	skin_detected0 = cv2.GaussianBlur(skin_detected0, (3, 3), 0)
	skin_detected0 = 255 * (np.uint8(skin_detected0/150))

	#cv2.imshow('Mask', skin_detected0)

	frame_BGS_skin = cv2.bitwise_and(frame_BGS_input, frame_BGS_input, mask=skin_detected)	
	frame_skin = cv2.bitwise_and(frame_input, frame_input, mask=skin_detected0)	
	#cv2.imshow('Hand', frame_skin)
	#cv2.imshow('HandA', frame_BGS_skin)
	
	return frame_skin, frame_BGS_skin


