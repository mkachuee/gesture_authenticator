"""
This module implements phase1 of the project
"""
# imports
import pdb

import numpy as np
import cv2

# options

def remove_background(frame_background, frame_input):
    """
    This function removes background from the frame_input
    """
    frame_background_gray = cv2.cvtColor(frame_background, cv2.COLOR_BGR2GRAY)
    frame_input_gray = cv2.cvtColor(frame_input, cv2.COLOR_BGR2GRAY)
    # remove background
    frame_output_4 = np.uint8(
        np.abs(np.int_(frame_background_gray) -np.int_(frame_input_gray)))
    # convert to binary image
    ret, frame_output_5 = cv2.threshold(frame_output_4, 64, 255, cv2.THRESH_BINARY)

    # extra precessings
    #frame_output_gaussian = cv2.GaussianBlur(frame_output_6, (3, 3), 0, 0)
    
    # median of image to remove salt and papper noise
    frame_median = cv2.medianBlur(frame_output_5, 3)
    
    # crop image
    median_gray = frame_median#cv2.cvtColor(frame_median, cv2.COLOR_BGR2GRAY)
    ind = np.nonzero(median_gray)
    frame_cropped = np.array([[0, 0],[0, 0]])
    frame_in_cropped = np.array([[0, 0],[0, 0]])
    crop_point = (-1, -1)
    if len(ind[0]) !=0:
        crop_point = (np.min(ind[0]), np.min(ind[1]))
        frame_in_cropped = frame_input[np.min(ind[0]):np.max(ind[0]), 
            np.min(ind[1]):np.max(ind[1]), :]
        frame_cropped = frame_output_5[np.min(ind[0]):np.max(ind[0]), 
            np.min(ind[1]):np.max(ind[1])]
    if frame_cropped.shape[0]==0 or frame_cropped.shape[1]==0:
        frame_cropped = np.array([[0, 0],[0, 0]])
        frame_in_cropped = np.array([[0, 0],[0, 0]])
    # handle empty frames
    if np.all(frame_cropped == np.array([[0, 0],[0, 0]])):
        return crop_point, frame_cropped, frame_in_cropped
    
    # do dilation
    kernel =np.ones((9, 7), np.uint8)# cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,2))
    #kernel_1 =np.ones((8, 4), np.uint8)# cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,2))
    #kernel_2 =np.ones((12, 2), np.uint8)# cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,2))
    frame_dilate = cv2.dilate(frame_cropped, kernel)
    #frame_dilate_erode = cv2.erode(frame_dilate, kernel_2)
    

    frame_mask = frame_dilate

    frame_output = np.tile(frame_mask.transpose()/255, \
        (3, 1, 1)).transpose() * frame_in_cropped
    
    return crop_point, frame_output, frame_cropped

