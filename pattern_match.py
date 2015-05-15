"""
This module implements phase4 of the project
"""
# imports
import pdb

import numpy as np
import cv2

# options

def match_pattern(pattern, list_keys):
    """
    This function matches a pattern with a list of keys
    """
    output = 'Not Found'
    output_ind = -1
    scores = []

    for key in list_keys:
	positive_pixels = 0
	total_pattern_pixels = 0
	total_key_pixels = 0
	key_size = key[1].shape
        pattern_resized = cv2.resize(pattern, key_size)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
	key_dilated = cv2.dilate(key[1], kernel, iterations=2)
	pattern_true_pixel = cv2.bitwise_and(pattern_resized, pattern_resized, mask=key_dilated)
	for x in range(0,key_size[0]-1) :
		for y in range (0,key_size[0]-1) :
			if pattern_true_pixel.item(x, y) :
				positive_pixels += 1
			if pattern_resized.item(x, y) :
				total_pattern_pixels += 1
			if key[1].item(x, y) :
				total_key_pixels += 1
			 
        # calc score
        # frame of key pattern is in key[1]
        pattern_match = (positive_pixels / total_pattern_pixels)*100
        kay_match = (positive_pixels / total_key_pixels)*100
        pattern_score = min(pattern_match, kay_match)
        # add to score list
        scores.append(pattern_score)

    scores = np.vstack(scores)
    best_match = np.argmax(scores)

    if scores[best_match] > THRESHOLD:
        output = list_keys[best_match][0]
        output_ind = best_match
    return output, output_ind

