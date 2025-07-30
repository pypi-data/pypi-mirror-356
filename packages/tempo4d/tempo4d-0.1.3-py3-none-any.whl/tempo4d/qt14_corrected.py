# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 18:46:25 2024

@author: ardag
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import torch
from concurrent.futures import ThreadPoolExecutor
import os
import cv2
from .utils.auto_cc_norm_batch_log2 import log_autocorrelation_2D_torch
from .utils.dspacing_batch5 import find_nearest_neighbors
from .utils.fit_index_batch2 import find_peaks
import logging
from ultralytics import YOLO
import threading
import time

lock = threading.Lock()
logging.getLogger("ultralytics").setLevel(logging.WARNING)
# Global variables for strain data
a_values = None
b_values = None
nearest_distance_values = None
roi_coordinates = None  # To store ROI coordinates
new_fig = None
new_ax2 = None
new_rect_selector = None
strain_a_plot = None
strain_b_plot = None
im1 = None
ani = None
animation_complete = False


class DiffPlotWorker(QtCore.QObject):
    data_ready = QtCore.pyqtSignal(np.ndarray)
    finished = QtCore.pyqtSignal()

    def __init__(self, app_ref):
        super().__init__()
        self.app_ref = app_ref  # Reference to RealTimePlotApp

    @QtCore.pyqtSlot()
    def run(self):
        try:
            for a in self.app_ref.process_diff_plot():
                self.data_ready.emit(a)
        finally:
            self.finished.emit()


class YOLOModel:
    def __init__(self, weights_path, device='cuda'):
        """
        Initialize the YOLO model with the given weights and device.

        Args:
            weights_path (str): Path to the YOLO weights file.
            device (str): Device to run the model ('cuda' or 'cpu').
        """
        self.device = device
        self.model = YOLO(weights_path)
        self.model.to(self.device)

    def detect(self, img_batch, img_size=1024, conf_score=0.25, overlap_thr=0.1, save=False, save_txt=False, dynamic=False):
        """
        Perform object detection on a batch of images with optional dynamic grid reconstruction.
    
        Args:
            img_batch (list of np.array): Batch of images to process.
            img_size (int): Image size for inference.
            conf_score (float): Confidence threshold for detection.
            overlap_thr (float): Overlap threshold (IOU).
            save (bool): Whether to save detection results.
            save_txt (bool): Whether to save detection results as text.
            dynamic (bool): Whether to enable dynamic grid reconstruction.
    
        Returns:
            list: Detection results for the batch.
        """
        with lock:
            with torch.no_grad():
                with torch.cuda.amp.autocast():
                    results = self.model.predict(
                        source=img_batch,
                        imgsz=img_size,
                        conf=conf_score,
                        max_det=100,
                        iou=overlap_thr,
                        save_txt=save_txt,
                        verbose=False,
                        half=False,
                    )
        return results
    
from importlib.resources import path
from tempo4d import models  # assuming your weights are in data_processor/models

with path(models, "yolov8_weights.pt") as weights_path:
    yolo_model = YOLOModel(str(weights_path))


class RealTimePlotApp(QtWidgets.QMainWindow):
    def __init__(self, data, img_size, h, normalize, map_i, map_j, pixel_size, neighbours, conf, batch_size=32):
        super().__init__()

        self.data = data
        self.img_size = img_size
        self.h = h
        self.normalize = normalize
        self.map_i = map_i
        self.map_j = map_j
        self.pixel_size = pixel_size
        self.neighbours = neighbours
        self.sort_ccw = False
        self.conf = conf
        self.batch_size = batch_size
        self.a_values = None
        self.nearest_distance_values = None
        self.animation_complete = False
        # Create PyQtGraph window and plot
        self.setWindowTitle("Real-Time Plot")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a layout
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_widget.setBackground('#636300')   # Dark gray background
        self.layout.addWidget(self.graph_widget)

        # Add a plot and an image item
        pg.setConfigOptions(useOpenGL=True)
        self.plot_item = self.graph_widget.addPlot(title="Strain Map")
        #self.plot_item.enableAutoRange('xy', False)
        self.img_item = pg.ImageItem()
        self.plot_item.addItem(self.img_item)
        self.plot_item.setAspectLocked(True)
        
        # Invert the y-axis so updates start from the top-left
        view_box = self.plot_item.getViewBox()
        view_box.invertY(True)

        # Run processing in background thread
        self.thread = QtCore.QThread()
        self.worker = DiffPlotWorker(self)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.data_ready.connect(self.img_item_update)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.on_processing_finished)
        
        self.thread.start()
        
        # Record start time
        self.start_time = time.time()
        
        
    @QtCore.pyqtSlot()
    def on_processing_finished(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Total time to complete plot: {total_time:.2f} seconds")
        self.animation_complete = True
        
        
    @QtCore.pyqtSlot(np.ndarray)
    def img_item_update(self, data):
        self.img_item.setImage(data.T, autoLevels=True)
    
    def update_plot(self):


        try:
            data = next(self.data_gen)
            self.img_item.setImage(data.T, autoLevels=True)
        except StopIteration:
            self.timer.stop()
            # Record end time and calculate total elapsed time
        #end_time = time.time()
        #total_time = end_time - self.start_time
        #print(f"Total time to complete plot: {total_time:.2f} seconds")
            
    def process_slices_batch(self, batch_indices, batch_slices, image_size, h, normalize, pixel_size, neighbours, conf, model):
        batch_results = []
        try:
            processed_slices = []
            for img_slice in batch_slices:
                try:
                    img = cv2.normalize(img_slice, None, 0, 256, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    img = log_autocorrelation_2D_torch(img)
                    img = cv2.normalize(img, None, 0, normalize, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                    img_x = cv2.bitwise_not(img)
                    processed_slices.append(img_x)
                except Exception as e:
                    print(f"Error processing image slice: {e}")
                    processed_slices.append(None)
    
            try:
                results = model.detect(
                    processed_slices,
                    img_size=image_size,
                    conf_score=conf,
                    overlap_thr=0.1,
                    save=False,
                )
            except Exception as e:
                print(f"Error running model.detect: {e}")
                results = [None] * len(batch_indices)
    
            for idx, (i, j) in enumerate(batch_indices):
                try:
                    boxes = results[idx].boxes if results[idx] else None
                    bbox_xywh = boxes.xywh.tolist() if boxes else []
    
                    if not bbox_xywh or len(bbox_xywh) < neighbours:
                        #print(f"[Warning] Insufficient detections at ({i}, {j}). Filling with zeros.")
                        nearest_distances = [0] * neighbours
                        angles = [0] * neighbours
                        a = 0
                    else:
                        coords_r = find_peaks(batch_slices[idx], bbox_xywh)
                        nearest_distances, angles = find_nearest_neighbors(coords_r, pixel_size, num_neighbors=neighbours)
    
                        if len(nearest_distances) < neighbours:
                            nearest_distances += [0] * (neighbours - len(nearest_distances))
                            angles += [0] * (neighbours - len(angles))
    
                        nearest_distances = nearest_distances[:neighbours]
                        angles = angles[:neighbours]
    
                        h_safe = h if h < len(nearest_distances) else 0
                        a = nearest_distances[h_safe]
    
                    batch_results.append((i, j, a, nearest_distances, angles))
    
                except Exception as e:
                    #print(f"Error processing results for batch index ({i}, {j}): {e}")
                    batch_results.append((i, j, 0, [0] * neighbours, [0] * neighbours))
    
        except Exception as e:
            print(f"Critical error in process_slices_batch: {e}")
    
        return batch_results



    def process_diff_plot(self):
        a = np.zeros((self.map_i, self.map_j))
        nearest_distances = np.zeros((self.map_i, self.map_j, self.neighbours))
        angles_map = np.zeros((self.map_i, self.map_j, self.neighbours))
    
        num_workers = os.cpu_count()
    
        def data_generator():
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                batch_indices = []
                batch_slices = []
                for i in range(self.data.shape[0]):
                    for j in range(self.data.shape[1]):
                        img_slice = self.data[i, j]
                        batch_indices.append((i, j))
                        batch_slices.append(img_slice)
    
                        if len(batch_indices) == self.batch_size:
                            futures.append(executor.submit(
                                self.process_slices_batch,
                                batch_indices, batch_slices,
                                self.img_size, self.h, self.normalize,
                                self.pixel_size, self.neighbours, self.conf, yolo_model
                            ))
                            batch_indices, batch_slices = [], []
    
                if batch_indices:
                    futures.append(executor.submit(
                        self.process_slices_batch,
                        batch_indices, batch_slices,
                        self.img_size, self.h, self.normalize,
                        self.pixel_size, self.neighbours, self.conf, yolo_model
                    ))
    
                for future in futures:
                    batch_results = future.result()
                    for (i, j, a_val, nearest_distance_val, angle_vals) in batch_results:
                        expected_length = self.neighbours
    
                        if len(nearest_distance_val) < expected_length:
                            nearest_distance_val = list(nearest_distance_val) + [0] * (expected_length - len(nearest_distance_val))
                        if len(angle_vals) < expected_length:
                            angle_vals = list(angle_vals) + [0] * (expected_length - len(angle_vals))
    
                        nearest_distances[i, j, :] = nearest_distance_val[:expected_length]
                        angles_map[i, j, :] = angle_vals[:expected_length]
                        a[i, j] = a_val
    
                    self.a_values = a
                    self.nearest_distance_values = nearest_distances
                    self.angles = angles_map
    
                    yield a
    
        return data_generator()


    def run(self):
        if not self.animation_complete:
            QtWidgets.QApplication.instance().exec_()  # Access the current QApplication instance
        return self.nearest_distance_values, self.angles


# Example Usage
if __name__ == "__main__":
    app = QtWidgets.QApplication([])




