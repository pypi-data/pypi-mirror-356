# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:52:03 2025

@author: ardag
"""

# data_process.py

from .bf_image import BF
from .data_process_gauss import object_detection_test, plot_coordinates
from .qt14_corrected import RealTimePlotApp
from .strain_analysis_post3 import post_main


class DataProcessor:
    def __init__(self, data=None, pixel_size=None, path_to_image=None,
                 nearest_distance_values=None, angles=None):
        """
        Initialize the processor with optional raw data, pixel size,
        background image path, and optionally precomputed strain data.
        """
        self.data = data
        self.pixel_size = pixel_size
        self.path_to_image = path_to_image
        self.image_bf = None
        self.detected_coords = None
        self.nearest_distance_values = nearest_distance_values
        self.angles = angles
        self.strain_output = None

    def generate_bf_image(self, disk_size=2):
        row = self.data.shape[2] // 2
        col = self.data.shape[3] // 2
        self.image_bf = BF(self.data, row, col, self.data.shape[0], self.data.shape[1], disk_size)
        return self.image_bf

    def run_object_detection(self, i=10, j=10, normalize1=256, normalize2=200,
                             img_size=640, conf_score=0.1, radius=1, neighbours=8):
        self.detected_coords = object_detection_test(
            self.data, i, j, normalize1, normalize2, self.path_to_image,
            img_size=img_size, conf_score=conf_score, radius=radius,
            save=False, s_txt=False, auto_cc=True
        )
        plot_coordinates(self.detected_coords, neighbours)
        return self.detected_coords

    def launch_realtime_plot(self, image_size=512, h=4, normalize=100,
                             neighbours=8, conf=0.01, batch_size=64):
        from PyQt5.QtWidgets import QApplication
        map_i, map_j = self.data.shape[0], self.data.shape[1]

        app = QApplication.instance()
        if not app:
            app = QApplication([])

        main_app = RealTimePlotApp(self.data, image_size, h, normalize,
                                   map_i, map_j, self.pixel_size,
                                   neighbours, conf, batch_size)
        main_app.show()
        self.nearest_distance_values, self.angles = main_app.run()
        return self.nearest_distance_values, self.angles

    def postprocess_strain(self, h=4, k=7, hk=0, rotation=4, axis_parm=1,
                           image_path=None, save=False):
        """Run the strain postprocessing pipeline."""
        if self.nearest_distance_values is None or self.angles is None:
            raise ValueError("Run `launch_realtime_plot()` first to generate strain and angle data.")

        img_path = image_path if image_path else self.path_to_image
        self.strain_output = post_main(
            self.nearest_distance_values,
            self.angles,
            rotation,
            h, k, hk,
            axis_parm,
            img_path,
            save=save
        )

    
__all__ = ["DataProcessor"]
