# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:44:59 2024

@author: ardag
"""

import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
from .utils.auto_cc_norm_batch_log2 import log_autocorrelation_2D_torch


def object_detection_test(data, i, j, normalize1, normalize2, path_to_image, img_size=1024, conf_score=0.01, radius=15, save = False, s_txt = False, auto_cc = False, gauss=False, cm=False):
   
    img = data[i, j, :, :]
    img= cv2.normalize(img, None, 0, normalize1, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    if auto_cc == True:
        #img = normalized_autocorrelation_2D_single(img)
        img = log_autocorrelation_2D_torch(img)
    img= cv2.normalize(img, None, 0, normalize2, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img =  cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_x =cv2.bitwise_not(img)
    from importlib.resources import path
    from tempo4d import models  # assuming your weights are in data_processor/models

    with path(models, "yolov8_weights.pt") as weights_path:
       model = YOLO(str(weights_path))

       model.to('cuda')
    
    # Run detection on the image
    results = model.predict(source=img_x, imgsz=img_size, conf=conf_score, max_det=100, iou=0.01, save_txt = s_txt)
    
    # Get bounding boxes
    boxes = results[0].boxes
    bbox_xyxy = boxes.xyxy.tolist()
    #bbox_xywh = boxes.xywh.tolist()
    
    #bbox_xywh = xyxy2xywh(np.asarray(bbox_xyxy))
    # Convert bounding boxes from xyxy to xywh
    
    bbox_xywh = []
    for bbox in bbox_xyxy:
       x1, y1, x2, y2 = bbox

       x_center = ((x1+x2) / 2) - 0.5
       y_center = ((y1+y2) / 2) - 0.5
       width = x2 - x1
       height = y2 - y1
       bbox_xywh.append([x_center, y_center, width, height])
    
    bbox_xywh = np.array(bbox_xywh)
    
    if gauss == True:
        from fit_index_batch import custom_find_peaks
        coords = custom_find_peaks(img, bbox_xyxy, bbox_xywh, com=False, gfit=True)
    if cm == True:
        from fit_index_batch import custom_find_peaks
        coords = custom_find_peaks(img, bbox_xyxy, bbox_xywh, com=True, gfit=False)
    else:
        coords = bbox_xywh[:, :2]
    def show_points(coords, ax, marker_size=1):
        ax.scatter(coords[:, 0], coords[:, 1], color='red', marker='.', s=marker_size, edgecolor='white', linewidth=0)
        """
        for coord in coords:
            circle = plt.Circle(coord, radius, color='red', fill=False, linewidth=1.25)
            ax.add_patch(circle)
            """
    # Create a figure with two subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 8))
    
    # Plot the object detection results on the first subplot
    #img= cv2.normalize(img, None, 0, 300, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    ax1.imshow(img)
    ax1.set_title('Pattern', fontsize=26, fontweight='bold')
    ax1.axis('off')
    
    ax2.imshow(img)
    for bbox in bbox_xywh:
        
        rect = plt.Rectangle((bbox[0] - (bbox[2] / 2) , bbox[1] - (bbox[3] / 2)), bbox[2], bbox[3], linewidth=2, edgecolor='red', facecolor='none')
        ax2.add_patch(rect)
    ax2.set_title('Detection', fontsize=26, fontweight='bold')
    ax2.axis('off')
    
    # Plot the points on the second subplot
    ax3.imshow(img)
    show_points(coords, ax3)
    #ax3.set_title('Center Points')
    ax3.axis('off')
    plt.tight_layout()
    
    if save == True:
        plt.imsave(path_to_image, img_x)
    
    plt.show()
    return coords



def plot_coordinates(coords_r, num_neighbors=1):
    """
    Find the nearest neighbors of the point closest to the centroid of a set of coordinates.
    
    Parameters:
    - coords_r: np.ndarray, array of coordinates with shape (n, 2)
    - pixel_size: float, the pixel size used for distance calculations
    - num_neighbors: int, the number of nearest neighbors to find (default is 1)
    
    Returns:
    - selected_index: int, index of the selected point closest to the centroid
    - nearest_indices: np.ndarray, indices of the nearest neighbors
    - dspacing: np.ndarray, corresponding d-spacings for the nearest neighbors
    """
    # Calculate the centroid of the coordinates
    centroid = np.mean(coords_r, axis=0)

    # Calculate distances from the centroid to each coordinate
    distances_from_centroid = np.linalg.norm(coords_r - centroid, axis=1)

    # Find the index of the coordinate closest to the centroid
    selected_index = np.argmin(distances_from_centroid)

    # Calculate distances from the selected point to all other points
    selected_point = coords_r[selected_index]
    selected_distances = np.linalg.norm(coords_r - selected_point, axis=1) 
    
    # Get the indices of the nearest neighbors, excluding the point itself
    nearest_indices = np.argsort(selected_distances)[1:num_neighbors + 1]
    
    # Get the corresponding distances of the nearest neighbors
    """
    plt.scatter(coords_r[:, 0], coords_r[:, 1], color='blue', label='Original Points')
    plt.scatter(coords_r[selected_index, 0], coords_r[selected_index, 1], color='red', label='Selected Point')
    plt.scatter(coords_r[nearest_indices, 0], coords_r[nearest_indices, 1], color='green', label='Nearest Neighbors')
    plt.legend()
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Original Points and Nearest Neighbors')
    plt.tight_layout()
    plt.show()

    """
    plt.scatter(coords_r[:, 0], coords_r[:, 1], color='blue', label='Original Points', alpha=0.5)
    plt.scatter(coords_r[selected_index, 0], coords_r[selected_index, 1], color='red', label='Selected Point')
    
    # Colormap for neighbors
    colors = plt.cm.turbo(np.linspace(0, 1, len(nearest_indices)))
    
    for idx, (neighbor_idx, color) in enumerate(zip(nearest_indices, colors), start=1):
        plt.scatter(coords_r[neighbor_idx, 0], coords_r[neighbor_idx, 1], color='yellow', label=f'Neighbor {idx}')
        plt.text(coords_r[neighbor_idx, 0] +6, coords_r[neighbor_idx, 1], str(idx-1), color=color, fontsize=16, weight='bold')

    #plt.legend()
    plt.title('Centers', fontsize=26, fontweight='bold')
    #plt.xlabel('X Coordinate')
    #plt.ylabel('Y Coordinate')
    plt.axis("off")
    plt.show()

