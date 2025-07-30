# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:09:27 2025

@author: ardag
"""

# data_manager.py
from .utils.loadtxt3 import load_data 
from .utils.savetxt2 import save_data
from .utils.data_reader import load as load_4d_data

class DataManager:
    def __init__(self, load_path=None, save_path=None):
        self.load_path = load_path
        self.save_path = save_path
        self.data = None
        self.processed_data = None
        self.data_4d = None

    def load(self):
        self.data = load_data(self.load_path)

    def process(self, post_fn):
        """Apply an external postprocessing function to self.data"""
        self.processed_data = post_fn(self.data)

    def save(self):
        save_data(self.processed_data, self.save_path)


__all__ = ["DataManager", "load_data", "save_data", "load_4d_data"]

