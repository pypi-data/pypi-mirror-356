# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:58:21 2024

@author: ardag
"""



import numpy as np

def find_nearest_neighbors(boxes_xywh, pixel_size, num_neighbors=1):
    """
    Find the nearest neighbors of the point closest to the centroid and compute their
    orientation angles relative to the x-axis, wrapped to [0, 2π).

    Parameters:
    - boxes_xywh: np.ndarray of shape (n, 4), bounding boxes in [x_center, y_center, w, h] format
    - pixel_size: float, pixel size in Å/pixel
    - num_neighbors: int, number of nearest neighbors to return

    Returns:
    - dspacing: np.ndarray of shape (num_neighbors,), corresponding d-spacings in Å
    - angles_fixed: np.ndarray of shape (num_neighbors,), angles in radians in [0, 2π)
    """

    # Step 0: Extract coordinates from detection boxes
    coords_r = np.array([(box[0], box[1]) for box in boxes_xywh])

    if coords_r.shape[0] < num_neighbors + 1:
        raise ValueError(f"[Error] Not enough detected spots: {coords_r.shape[0]} vs {num_neighbors + 1}")

    # Step 1: find the center spot closest to the geometric centroid
    centroid = np.mean(coords_r, axis=0)
    distances_from_centroid = np.linalg.norm(coords_r - centroid, axis=1)
    selected_index = np.argmin(distances_from_centroid)
    selected_point = coords_r[selected_index]

    # Step 2: find the nearest neighbors to that point
    selected_distances = np.linalg.norm(coords_r - selected_point, axis=1)
    neighbor_indices = np.argsort(selected_distances)[1:num_neighbors + 1]
    neighbor_coords = coords_r[neighbor_indices]
    neighbor_distances = selected_distances[neighbor_indices]

    # Step 3: compute Bragg vectors
    vectors = neighbor_coords - selected_point

    # Step 4: flip vectors to align consistently with the global x-axis (right)
    ref_vec = np.array([1.0, 0.0])  # fixed x-axis reference
    aligned_vectors = np.array([
        v if np.dot(v, ref_vec) >= 0 else -v for v in vectors
    ])

    # Step 5: compute orientation angles relative to x-axis, in [0, 2π)
    angles_fixed = np.arctan2(aligned_vectors[:, 1], aligned_vectors[:, 0])
    angles_fixed = (angles_fixed + 2 * np.pi) % (2 * np.pi)

    # Step 6: compute d-spacings
    dspacing = 1 / (neighbor_distances * pixel_size)

    return dspacing.tolist(), angles_fixed.tolist()






