"""
This module detects active hand and returns it
"""

# imports
import pdb

import numpy as np
import cv2

# options


def find_active_hand(frame_input):
    frame_input_gray = cv2.cvtColor(frame_input, cv2.COLOR_BGR2GRAY)
    frame_bin = cv2.threshold(
        frame_input_gray, 32, 255, cv2.THRESH_BINARY)[1]
    # do some dilation
    kernel =np.ones((9, 9), np.uint8)
    frame_bin = cv2.dilate(frame_bin, kernel)
    # find contours
    (cnts, _) = cv2.findContours(
        frame_bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
    frame_contours = frame_input.copy()
    cv2.drawContours(frame_contours, cnts, -1, (0,255,0), 3)
    # find active hand
    frame_cropped = np.array([[255, 255], [255, 255]])
    # detect it
    crop_point = (-1, -1)
    if len(cnts) > 1:
        cnt_act = cnts[1]
        # find bounding box
        p1 = np.min(cnt_act, axis=0)
        p2 = np.max(cnt_act, axis=0)
        # find active hand
        if len(cnts) > 2:    
            p01 = np.min(cnts[2], axis=0)
            p02 = np.max(cnts[2], axis=0)
            if p01[0, 1] < p1[0, 1]:
                p1 = p01
                p2 = p02

        frame_cropped = \
            frame_input[p1[0, 1]:p2[0, 1], p1[0, 0]:p2[0, 0], :]
        crop_point = (p1[0, 0], p1[0, 1])
    else:
        pass
    frame_output = frame_cropped

    
    if np.min(frame_output.shape) < 2:
        crop_point = (-1, -1)
        frame_output = np.array([[255, 255], [255, 255]])

    return crop_point, frame_output, frame_contours
