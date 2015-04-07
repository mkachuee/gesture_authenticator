"""
This module implements face detection function
"""
# imports

import numpy as np
import cv2


def face_detect(image_input):
	
	face_cascade = cv2.CascadeClassifier(
            '../../SmartVision/haarcascade_frontalface_default.xml')
	#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

	gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	#image_output = image_input.copy()
	#for (x, y, w, h) in faces:
	#		cv2.rectangle(image_output, (x, y) , (x+w, y+h), (255, 0, 0), 2)
	#return image_output
	return faces
