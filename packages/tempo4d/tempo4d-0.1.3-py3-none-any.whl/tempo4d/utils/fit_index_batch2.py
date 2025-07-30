# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:53:34 2024

@author: ardag
"""

import numpy as np


def find_peaks(img, boxes_xywh):

    
    coords = []
    
    for i in range(len(boxes_xywh)):
        center_x, center_y = boxes_xywh[i][:2]
        coords.append((center_x, center_y))
    
    coords = np.array(coords)
    

    return coords
    
