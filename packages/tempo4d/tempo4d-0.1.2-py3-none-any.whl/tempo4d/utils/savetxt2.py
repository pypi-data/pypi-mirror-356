# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 07:26:40 2024

@author: ardag
"""

import numpy as np

def save_data(filename, nearest_distance_values_param, angles_param=None):
    """
    Save d-spacings and optionally angles to a CSV file.

    Parameters:
    - filename: str, path to save the .csv file
    - nearest_distance_values_param: np.ndarray, shape (i, j, n), d-spacing values
    - angles_param: np.ndarray or None, shape (i, j, n), orientation angles in degrees (optional)
    """
    nearest_distance_values = nearest_distance_values_param
    flat_nearest_distances = nearest_distance_values.reshape(-1, nearest_distance_values.shape[-1])
    
    row_col_indices = np.indices((nearest_distance_values.shape[0], nearest_distance_values.shape[1])).reshape(2, -1).T
    
    if angles_param is not None:
        flat_angles = angles_param.reshape(-1, angles_param.shape[-1])
        data_to_save = np.hstack((row_col_indices, flat_nearest_distances, flat_angles))
        header = 'Row,Col,' + \
                 ','.join([f'Dist{i+1}' for i in range(flat_nearest_distances.shape[1])]) + ',' + \
                 ','.join([f'Angle{i+1}' for i in range(flat_angles.shape[1])])
    else:
        data_to_save = np.hstack((row_col_indices, flat_nearest_distances))
        header = 'Row,Col,' + ','.join([f'Dist{i+1}' for i in range(flat_nearest_distances.shape[1])])

    np.savetxt(filename, data_to_save, delimiter=',', header=header, comments='', fmt='%.6f')
