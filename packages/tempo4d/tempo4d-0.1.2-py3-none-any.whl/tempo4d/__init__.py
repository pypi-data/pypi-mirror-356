# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 20:10:26 2025

@author: ardag
"""

# data_processor/__init__.py

from .data_manager import DataManager, load_data, save_data
from .data_process import DataProcessor  # import the class

__all__ = [
    "DataManager",
    "DataProcessor",
    "load_data",
    "save_data"
]

