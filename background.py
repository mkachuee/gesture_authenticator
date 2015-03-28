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
    frame_output_6 = np.tile(frame_output_5.transpose()/255, (3, 1, 1)).transpose() * frame_input
    return frame_output_6

