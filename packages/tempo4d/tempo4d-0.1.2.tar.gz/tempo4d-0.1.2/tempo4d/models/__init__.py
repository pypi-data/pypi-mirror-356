# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 09:45:36 2025

@author: ardag
"""

"""
This module provides access to pre-trained model weights.
"""

import importlib.resources
import torch

def load_yolov8_weights(map_location="cpu"):
    """
    Loads the YOLOv8 PyTorch model weights from the package.

    Args:
        map_location (str): Where to load the weights (e.g., 'cpu' or 'cuda').

    Returns:
        torch.nn.Module or state_dict: The loaded model weights.
    """
    with importlib.resources.path(__package__, "yolov8_weights.pt") as path:
        return torch.load(path, map_location=map_location)

__all__ = ["load_yolov8_weights"]