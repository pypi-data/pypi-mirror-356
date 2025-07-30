# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:50:34 2024

@author: ardag
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from strain_clean import clean_strain_data
import csv
import os

# Global variables for strain data
nearest_distance_values = None
roi_coordinates = None  # To store ROI coordinates
rect_selector = None
new_fig = None
new_strain_a = None
new_strain_b = None
ax_plot = None

def onselect(eclick, erelease):
    global roi_coordinates, ax1
    roi_coordinates = (int(eclick.xdata), int(eclick.ydata), int(erelease.xdata), int(erelease.ydata))
    print(f"ROI selected from ({roi_coordinates[0]}, {roi_coordinates[1]}) to ({roi_coordinates[2]}, {roi_coordinates[3]})")
    
    for text in ax1.texts:
            text.remove()
    text_x = (roi_coordinates[0] + roi_coordinates[2]) / 2
    text_y = roi_coordinates[1] - 1  # Adjust the vertical position above the ROI
    ax1.text(text_x, text_y, 'Reference', fontsize=8, color='black', ha='center', va='bottom', bbox=dict(facecolor='green', alpha=0.2))
    ax1.figure.canvas.draw() 
    
def on_key(event):
    if event.key == 'enter':
        calculate_new_strain()

def setup_roi_selector(fig, ax1):
    global rect_selector
    rect_selector = RectangleSelector(ax1, onselect, useblit=True, interactive=True, props=dict(facecolor='green', edgecolor='green', alpha=0.3, fill=True))
    rect_selector.set_active(True)  # Activate the ROI selector
    fig.canvas.mpl_connect('key_press_event', on_key)  # Connect key press event

def calculate_new_strain():
    global nearest_distance_values, roi_coordinates, new_fig
    global new_strain_a, new_strain_b, new_strain_c
    global new_rect_selector, new_ax1

    if roi_coordinates is not None:
        x1, y1, x2, y2 = roi_coordinates
        new_a0 = np.mean(nearest_distance_values[y1:y2, x1:x2, h])
        new_b0 = np.mean(nearest_distance_values[y1:y2, x1:x2, k])
        new_c0 = np.mean(nearest_distance_values[y1:y2, x1:x2, hk])

        print(f'new a0: {new_a0:.5f}, b0: {new_b0:.5f}, c0: {new_c0:.5f}')

        new_strain_a = (nearest_distance_values[:, :, h] - new_a0) / new_a0
        new_strain_b = (nearest_distance_values[:, :, k] - new_b0) / new_b0
        new_strain_c = (nearest_distance_values[:, :, hk] - new_c0) / new_c0

        # Plotting
        new_fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

        im1 = ax1.imshow(new_strain_a, cmap='bwr', vmin=-0.03, vmax=0.03)
        ax1.set_title('$\epsilon_{xx}$', fontsize=24)
        ax1.axis('off')
        new_fig.colorbar(im1, ax=ax1).set_label('Strain', fontsize=14)

        im2 = ax2.imshow(new_strain_b, cmap='bwr', vmin=-0.03, vmax=0.03)
        ax2.set_title('$\epsilon_{yy}$', fontsize=24)
        ax2.axis('off')
        new_fig.colorbar(im2, ax=ax2).set_label('Strain', fontsize=14)

        im3 = ax3.imshow(new_strain_c, cmap='bwr', vmin=-0.03, vmax=0.03)
        ax3.set_title('$\epsilon_{xy}$', fontsize=24)
        ax3.axis('off')
        new_fig.colorbar(im3, ax=ax3).set_label('Strain', fontsize=14)

        # ROI selector on second axis
        new_ax1 = ax1
        new_rect_selector = RectangleSelector(new_ax1, new_onselect, useblit=True, interactive=True,
                                              props=dict(facecolor='blue', edgecolor='blue', alpha=0.3, fill=True))
        new_rect_selector.set_active(True)
        new_fig.canvas.mpl_connect('key_press_event', new_on_key)

        plt.tight_layout()
        plt.show()


def new_onselect(eclick, erelease):
    global roi_coordinates, new_ax1
    roi_coordinates = (int(eclick.xdata), int(eclick.ydata), int(erelease.xdata), int(erelease.ydata))
    print(f"New ROI selected from ({roi_coordinates[0]}, {roi_coordinates[1]}) to ({roi_coordinates[2]}, {roi_coordinates[3]})")
    
    for text in new_ax1.texts:
            text.remove()
    text_x = (roi_coordinates[0] + roi_coordinates[2]) / 2
    text_y = roi_coordinates[1] - 1  # Adjust the vertical position above the ROI
    new_ax1.text(text_x, text_y, 'Line profile', fontsize=8, color='black', ha='center', va='bottom', bbox=dict(facecolor='blue', alpha=0.2))
    new_ax1.figure.canvas.draw() 
    
def new_on_key(event):
    if event.key == 'd':
        plot_line_profiles()

def plot_line_profiles():
    global roi_coordinates, new_strain_a, snew_strain_b, new_strain_c, axis_plot

    if roi_coordinates is not None:
        x1, y1, x2, y2 = roi_coordinates
        x1, x2 = max(0, x1), min(new_strain_b.shape[1], x2)
        y1, y2 = max(0, y1), min(new_strain_b.shape[0], y2)

        roi_xx = new_strain_a[y1:y2, x1:x2]
        roi_yy = new_strain_b[y1:y2, x1:x2]
        roi_xy = new_strain_c[y1:y2, x1:x2]

        # Line profiles: mean across axis
        line_profile_xx = np.nanmean(roi_xx, axis=axis_plot)
        line_profile_yy = np.nanmean(roi_yy, axis=axis_plot)
        line_profile_xy = np.nanmean(roi_xy, axis=axis_plot)

        # Precision estimates
        precision_xx = np.nanstd(line_profile_xx, ddof=1)
        precision_yy = np.nanstd(line_profile_yy, ddof=1)
        precision_xy = np.nanstd(line_profile_xy, ddof=1)
        
        print(f"Precision Exx: {precision_xx:.1e}")
        print(f"Precision Eyy: {precision_yy:.1e}")
        print(f"Precision Exy: {precision_xy:.1e}")

        # Plot line profiles
        fig, axs = plt.subplots(1, 3, figsize=(16, 4))

        axs[0].plot(line_profile_xx, linewidth=2)
        axs[0].set_ylim(-0.01, 0.04)
        axs[0].set_title('$\epsilon_{xx}$', fontsize=12)
        axs[0].set_xlabel('Distance (nm)', fontsize=8)
        axs[0].set_ylabel('Mean Strain', fontsize=8)

        axs[1].plot(line_profile_yy, linewidth=2)
        axs[1].set_ylim(-0.01, 0.04)
        axs[1].set_title('$\epsilon_{yy}$', fontsize=12)
        axs[1].set_xlabel('Distance (nm)', fontsize=8)
        axs[1].set_ylabel('Mean Strain', fontsize=8)

        axs[2].plot(line_profile_xy, linewidth=2)
        axs[2].set_ylim(-0.01, 0.04)
        axs[2].set_title('$\epsilon_{xy}$ (Shear)', fontsize=12)
        axs[2].set_xlabel('Distance (nm)', fontsize=8)
        axs[2].set_ylabel('Mean Strain', fontsize=8)

        plt.tight_layout()
        plt.show()

        # === Export to CSV ===
        output_filename = "strain_line_profiles.csv"
        with open(output_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Distance_Index", "Eyy", "Exx", "Exy"])
            for i in range(len(line_profile_yy)):
                writer.writerow([i, line_profile_yy[i], line_profile_xx[i], line_profile_xy[i]])

        print(f"Line profiles exported to: {os.path.abspath(output_filename)}")
    else:
        print("Strain data is not available yet.")

def post_main(nearest_distance_values_param, angles_param, rotation, h_param, k_param, hk_param, axis_parm, path_to_image, save=False):
    global nearest_distance_values, map_i, map_j, h, k, hk, ax1, axis_plot

    nearest_distance_values = nearest_distance_values_param
    map_i = nearest_distance_values_param.shape[0]
    map_j = nearest_distance_values_param.shape[1]
    h = h_param
    k = k_param
    hk = hk_param
    axis_plot = axis_parm

    # Extract displacements and clean
    displacements_a = clean_strain_data(nearest_distance_values[:, :, h], threshold=1.0)
    displacements_b = clean_strain_data(nearest_distance_values[:, :, k], threshold=1.0)

    # Compute orientation from angles
    orientation_map = angles_param[:, :, rotation]  # use angle of the h-th nearest neighbor
    orientation_map = np.unwrap(orientation_map, axis=0)
    orientation_map = np.unwrap(orientation_map, axis=1)

    # Convert angles to degrees in [0, 180) for visualization
    orientation_map_deg = np.degrees(orientation_map) % 180


    # Create subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    plt.subplots_adjust(left=0.1, bottom=0.25)

    # Plot Displacements A
    im1 = ax1.imshow(displacements_a, cmap='turbo_r')
    ax1.set_title('Displacements, h (nm)')
    ax1.axis('off')
    fig.colorbar(im1, ax=ax1)

    # Plot Displacements B
    im2 = ax2.imshow(displacements_b, cmap='turbo_r')
    ax2.set_title('Displacements, k (nm)')
    ax2.axis('off')
    fig.colorbar(im2, ax=ax2)

    
    # Plot the orientation map
    im3 = ax3.imshow(orientation_map_deg, cmap='hsv')
    ax3.set_title('Rotation (°)')
    ax3.axis('off')
    fig.colorbar(im3, ax=ax3, orientation='vertical')
    
    # Add below-map direction label
    ax3.text(0.5, -0.08, '← –x (0°) Bragg Vector Direction (180°) +x →',
             ha='center', va='center', fontsize=11, color='black', transform=ax3.transAxes)
    

    # === Layout adjustment to make space for label ===
    plt.tight_layout(rect=[0, 0.07, 1, 1])

    if save:
        plt.savefig(path_to_image, dpi=300)

    #plt.tight_layout()
    plt.show()
    setup_roi_selector(fig, ax1)
    return orientation_map_deg