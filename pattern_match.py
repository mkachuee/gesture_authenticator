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
        pattern_resized = cv2.resize(pattern, key[1].shape)
        # calc score
        # frame of key pattern is in key[1]
        pattern_score = 0.12345
        # add to score list
        scores.append(pattern_score)

    scores = np.vstack(scores)
    best_match = np.argmax(scores)

    if scores[best_match] > THRESHOLD:
        output = list_keys[best_match][0]
        output_ind = best_match
    return output, output_ind

