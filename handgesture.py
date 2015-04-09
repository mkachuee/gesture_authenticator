

# imports
import pdb

import numpy as np
import cv2


def detect_gesture(input_frame):
    # check the input
    if input_frame.shape[0] < 4:
        return input_frame
    # convert to binary
    frame_gray = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
    _, frame_bin = cv2.threshold(frame_gray, 100, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)







    return frame_bin
