

# imports
import pdb

import numpy as np
import cv2


def detect_gesture(input_frame):
    # check the input
    indicator = (-1, -1)
    est_gesture = -1
    if input_frame.shape[0] < 4:
        return input_frame, est_gesture, indicator
    # convert to binary
    frame_gray = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
    _, frame_bin = cv2.threshold(frame_gray, 32, 255, cv2.THRESH_BINARY)
    # find contours
    try:
        contours, hierarchy = cv2.findContours(
            frame_bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours = []
    # find the largest contour

    if len(contours) != 0:
        cnt = sorted(contours, key = cv2.contourArea, reverse = True)[0]
        # draw the convex hull
        hull = cv2.convexHull(cnt)
        cv2.drawContours(input_frame, [cnt], -1, (0,255,0), 2)
        cv2.drawContours(input_frame, [hull], -1, (0,0,255), 2)
        # find convexity defects
        cnt = cv2.approxPolyDP(cnt,0.025*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = np.zeros((0, 0))
        if hull.shape[0] > 3:
            defects = cv2.convexityDefects(cnt,hull)
        # draw defects
        try:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                #dist = cv2.pointPolygonTest(cnt,centr,True)
                cv2.line(input_frame,start,end,[0,255,0],2)
                cv2.circle(input_frame,far,5,[0,0,255],-1)
            #print(i+1)
            #print(input_frame.shape)
            # estimate hand gesture
            num_points = defects.shape[0]
            est_gesture = -1
            if num_points == 0:
                est_gesture = -1
            elif num_points <= 2:
                #pdb.set_trace()
                #print(cnt[defects[0, 0][2]][0][1])
                if cnt[defects[0, 0][2]][0][1] > 20 and \
                        np.abs(input_frame.shape[0]-input_frame.shape[1]) >5:
                    est_gesture = 2
                    #pdb.set_trace()
                    indicator = cnt[np.argmin(cnt, axis=0)[0, 1]][0]
                    cv2.circle(input_frame,tuple(indicator),5,[255,255,255],-1)
            elif num_points > 3:
                est_gesture=1
            #indicator = cnt[np.argmin(cnt, axis=0)[0, 1]][0]    
        except:
            pass#print(-1)


    return frame_bin, est_gesture, indicator
