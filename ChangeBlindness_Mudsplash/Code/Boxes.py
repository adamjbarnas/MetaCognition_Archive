#!/usr/bin/env python
# -*- coding: utf-8 -*-

#run with python

'''
This takes difference masks (generated by make_difference_masks.py) and draws a 
convex hull around the difference. This can be used as the correct location
when subjects are asked to click on what's different between two images. 
'''

import cv2 as cv
import numpy as np
import random as rng
import os

path = '/Users/adambarnas/Box/Mudsplash/Images/'
difference_mask_dir = '/Users/adambarnas/Box/Mudsplash/Masks'
bounding_box_dir = '/Users/adambarnas/Box/Mudsplash/Boxes'

#Create destination directory for bounding_boxes
if bounding_box_dir not in os.listdir(path):
    cmd = 'mkdir '+bounding_box_dir
    os.system(cmd)
else:
    pass


#Get the "stem" name for all images, e.g. rensink_Castle or wolfe_0110_L_plant 
stems = [item for item in os.listdir(path) if not item.startswith('.') 
        and item!=difference_mask_dir and item!=bounding_box_dir] #skips .DS_Store files

print(stems)
for stem in set(stems):
    print(stem)
    img = cv.imread(difference_mask_dir+'/'+stem+'_difference_mask.png',0)
    orig = cv.imread(path+'/'+stem+'/'+stem+'-a.jpg',3)

    cv.imshow('title',img)    


    threshold = 1
    # Detect edges using Canny
    canny_output = cv.Canny(img, threshold, threshold * 2)
    # Find contours
    #_, contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    ret,thresh = cv.threshold(img,127,255,0)
    contours,hierarchy = cv.findContours(thresh, 1, 2)

    # Find the convex hull object for each contour
    hull_list = []
    for i in range(len(contours)):
        hull = cv.convexHull(contours[i])
        hull_list.append(hull)
        
    # Draw contours + hull results
    contour_lengths = [c.shape[0] for c in contours]
    contour_lengths.sort()
    top4_longest = contour_lengths[-4:]


    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))

        # For some of the more complicated changes, more than one area needs to be defined
        if stem in []:
            longest = top4_longest
            showthis = True
        elif stem in ['rensink_Floatplane', 'rensink_BarnTrack', 'rensink_Chopper', 'rensink_Cockpit', 'rensink_Eating', 'rensink_Harbor', 'rensink_Turtle', 'ma_4247084', 'ma_69128765', 'ma_97475929', 'wolfe_image-005', 'wolfe_image-007', 'wolfe_image-023', 'wolfe_image-024', 'wolfe_image-079', 'wolfe_image-081', 'wolfe_image-082', 'wolfe_image-089', 'wolfe_image-092', 'wolfe_image-096', 'wolfe_image-099', 'wolfe_image-103', 'wolfe_image-111', 'wolfe_image-116', 'wolfe_003_L_ducks', 'wolfe_003_R_ducks', 'wolfe_009_L_carpet', 'wolfe_009_R_carpet', 'wolfe_024_L_towels', 'wolfe_024_R_towels', 'wolfe_077_L_footrest', 'wolfe_077_R_footrest', 'wolfe_082_L_bowl', 'wolfe_082_R_bowl']:
            longest = top4_longest[-6:] #changed from -2
            showthis = True
        else:
            longest = top4_longest[-1:]
            showthis = True

        if contours[i].shape[0] in longest:
            #cv.drawContours(drawing, hull_list, i, color)
            cnt = contours[i]
            hull = hull_list[i]
            cnt = np.int0(cnt)
            hull = np.int0(hull)

            #For Viewing
            cv.drawContours(orig, [cnt], 0, color,1)
            cv.drawContours(orig, [hull], 0, color,3) #3 for outline, -1 for fill

            # For Saving
            cv.drawContours(drawing, [hull], 0, (255,255,255),-1) #3 for outline, -1 for fill

            # cv2.drawContours(img,[box],0,(128,255,0),2)

    # Show in a window
    if showthis:
        cv.imshow('Contours', orig)
        #cv.waitKey(500)

    cv.imwrite(bounding_box_dir+'/'+stem+'_difference_hull.png',drawing)
    


