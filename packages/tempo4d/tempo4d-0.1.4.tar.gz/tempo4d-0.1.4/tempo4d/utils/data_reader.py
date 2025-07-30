# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:12:23 2024

@author: ardag
"""

from rsciio.digitalmicrograph import file_reader as dm_read
from rsciio.tia import file_reader as tia_read
from rsciio.empad import file_reader as empad_read
import os
import h5py
import numpy as np
import cv2

def convert_uint32_to_uint16(image_uint32):
    # Convert to float32 first (OpenCV-friendly)
    image_float = image_uint32.astype(np.float32)
    # Normalize to 0–65535
    img_norm = cv2.normalize(image_float, None, 0, 65535, cv2.NORM_MINMAX)
    return img_norm.astype(np.uint16)

def load(path):
    _, extension = os.path.splitext(path)
    if extension.lower() in ('.dm3', '.dm4'):        
        dm =  dm_read(path)
        pixel_size = round(dm[0]['original_metadata']["ImageList"]["TagGroup0"]["ImageData"]["Calibrations"]["Dimension"]["TagGroup0"]["Scale"],4)
        data = dm[0]["data"]
        if data.dtype == np.uint32:
         data = convert_uint32_to_uint16(data)
         
    if extension.lower() in ('.xml'):        
        emp =  empad_read(path)
        pixel_size = 0.062
        data = emp[0]["data"]

        
    if extension.lower() == '.de5':
        f = h5py.File(path,'r')
        data=f['4DSTEM_experiment']['data']['datacubes']['datacube_0']['data']
        data = np.asarray(data)
        pixel_size = 0.062
        
    if extension.lower() == '.emi':
        tia = tia_read(path)
        pixel_size = round(tia[0]['original_metadata']['ser_header_parameters']['CalibrationDeltaX'][0]*1e-9,3)
        data = tia[0]['data']
        
    if extension.lower() == '.hdf5':
        f = h5py.File(path,'r')
        data = f['data']
        data = np.asarray(data)
        pixel_size = 0.0609
    
    print(f"Data shape : {data.shape}")
    print(f"Pixel size (nm) : {pixel_size}")
    return data, pixel_size
