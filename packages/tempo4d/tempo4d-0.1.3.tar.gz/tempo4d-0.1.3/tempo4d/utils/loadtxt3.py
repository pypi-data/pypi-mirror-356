# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 07:30:14 2024

@author: ardag
"""
import numpy as np


def load_data(filename):
    """
    Load distances and angles from a CSV file saved by `save_data()`, and reshape them into 3D arrays.

    Parameters:
    - filename (str): Path to the CSV file.

    Returns:
    - nearest_distance_values: np.ndarray of shape (x, y, n)
    - angles: np.ndarray of shape (x, y, n), or None if angles not included
    """
    # Load the data, skipping header
    data = np.loadtxt(filename, delimiter=',', skiprows=1)

    # Extract row/col indices
    row_col_indices = data[:, :2].astype(int)
    rows = row_col_indices[:, 0]
    cols = row_col_indices[:, 1]

    # Infer 2D grid shape
    x = np.max(rows) + 1
    y = np.max(cols) + 1

    # Extract measurements
    values_flat = data[:, 2:]
    num_total_cols = values_flat.shape[1]

    # Assume half distance, half angles (if even number), else no angles
    if num_total_cols % 2 == 0:
        n = num_total_cols // 2
        nearest_distances_flat = values_flat[:, :n]
        angles_flat = values_flat[:, n:]
    else:
        n = num_total_cols
        nearest_distances_flat = values_flat
        angles_flat = None

    # Reshape back to original grid
    nearest_distance_values = nearest_distances_flat.reshape(x, y, n)
    angles = angles_flat.reshape(x, y, n) if angles_flat is not None else None

    print(f"Loaded distances shape: {nearest_distance_values.shape}")
    if angles is not None:
        print(f"Loaded angles shape: {angles.shape}")

    return nearest_distance_values, angles
