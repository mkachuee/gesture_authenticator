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
        pattern_resized = cv2.resize(pattern, (key[1].shape[1], key[1].shape[0]))
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
	key_dilated = cv2.dilate(key[1], kernel, iterations=2)
	#print (('key shape',key[1].shape))
	#print (('pattern shape',pattern_resized.shape))
	pattern_true_pixel = cv2.bitwise_and(pattern_resized, pattern_resized, mask=key_dilated)
	#cv2.imshow('dilated', key_dilated)
	#cv2.imshow('and', pattern_true_pixel)
	#print (('XxX',key_size[0]))
	#print (('YyY',key_size[1]))	
	#print (('PpP',pattern_true_pixel.shape))	
	#print (('KkK',key[1].shape))	
	for x in range(0,key_size[0]-1) :
		for y in range (0,key_size[1]-1) :
			if pattern_true_pixel.item(x, y) :
				positive_pixels += 1
			if pattern_resized.item(x, y) :
				total_pattern_pixels += 1
			if key[1].item(x, y) :
				total_key_pixels += 1
			 
        # calc score
	#print (('true',positive_pixels))
        #print (('pattern',total_pattern_pixels))
        #print (('key',total_key_pixels))
        # frame of key pattern is in key[1]
        pattern_match = (float(positive_pixels) / total_pattern_pixels)*100
        key_match = (float(positive_pixels) / total_key_pixels)*100
        pattern_score = min(pattern_match, key_match)
        # add to score list
        scores.append(pattern_score)
	print (('TestPercent',pattern_match))
        print (('PatternPercent',key_match))
	#print(pattern.shape)
    scores = np.vstack(scores)
    best_match = np.argmax(scores)
    print(('score', scores[best_match]))
    if scores[best_match] > 70:
        output = list_keys[best_match][0]
        output_ind = best_match
    return output, output_ind

