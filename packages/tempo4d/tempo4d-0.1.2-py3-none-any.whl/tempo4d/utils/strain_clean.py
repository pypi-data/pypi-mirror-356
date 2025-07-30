# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 10:16:59 2024

@author: ardag
"""

import numpy as np

def clean_strain_data(strain_data, threshold=1):
    """
    Clean strain data by replacing values that are too high compared to their neighbors.
    
    Parameters:
    - strain_data: np.ndarray, the strain data array
    - threshold: float, the maximum allowed ratio between a pixel value and the average of its neighbors
    
    Returns:
    - cleaned_strain_data: np.ndarray, the cleaned strain data array
    """
    cleaned_strain_data = strain_data.copy()
    rows, cols = strain_data.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Get the value of the current pixel
            current_value = strain_data[i, j]
            
            # Get the values of the 8 neighbors
            neighbors = [
                strain_data[i-1, j-1], strain_data[i-1, j], strain_data[i-1, j+1],
                strain_data[i, j-1],                       strain_data[i, j+1],
                strain_data[i+1, j-1], strain_data[i+1, j], strain_data[i+1, j+1]
            ]
            
            # Calculate the average value of the neighbors
            neighbors_avg = np.mean(neighbors)
            
            # Check if the current value is out of the allowed range
            if current_value > neighbors_avg * threshold:
                cleaned_strain_data[i, j] = neighbors_avg

    return cleaned_strain_data

# Example usage:
# strain_data = np.array([[...]])  # Your strain data array
# cleaned_data = clean_strain_data(strain_data)
