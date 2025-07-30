# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:29:05 2024

@author: ardag
"""

import numpy as np
import cv2

def pad_images(dataset, target_shape):
    """
    Pads a dataset of images to the target shape.
    
    Parameters:
    - dataset: np.ndarray, shape (n_batches, n_images, height, width), the input dataset.
    - target_shape: tuple, the target shape (height, width) to pad the images to.
    
    Returns:
    - padded_dataset: np.ndarray, the dataset with padded images.
    """
    dataset = cv2.normalize(dataset , None, 0,  256, cv2.NORM_MINMAX, dtype=cv2.CV_8U) 
    # Calculate the amount of padding required for height and width
    
    pad_height = (target_shape[0] - dataset.shape[2]) // 2
    pad_width = (target_shape[1] - dataset.shape[3]) // 2
    
    # Pad the dataset
    padded_dataset = np.pad(dataset, 
                            pad_width=((0, 0), (0, 0), (pad_height, pad_height), (pad_width, pad_width)), 
                            mode='constant', 
                            constant_values=0)
    print(f"Data shape : {padded_dataset.shape}")
    return padded_dataset
