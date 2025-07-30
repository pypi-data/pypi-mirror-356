# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 19:47:48 2025

@author: ardag
"""

import torch
import numpy as np


def log_autocorrelation_2D_torch(image_np: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """
    Compute the log-transformed normalized autocorrelation for a single 2D NumPy image using PyTorch,
    and return the result as a NumPy array.

    Parameters:
        image_np (np.ndarray): Input 2D image (H, W).
        epsilon (float): Small constant to avoid log(0).

    Returns:
        np.ndarray: Log-transformed, normalized autocorrelation (H, W).
    """
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    image_tensor = torch.tensor(image_np, dtype=torch.float32, device=device)

    H, W = image_tensor.shape

    # Remove DC offset
    image_centered = image_tensor - image_tensor.min()

    # FFT and power spectrum
    fft_image = torch.fft.fft2(image_centered)
    power_spectrum = torch.abs(fft_image) ** 2

    # Inverse FFT and shift
    autocorr = torch.fft.ifft2(power_spectrum).real
    autocorr_shifted = torch.fft.fftshift(autocorr)

    # Normalize to center
    center_value = autocorr_shifted[H // 2, W // 2]
    if center_value != 0:
        autocorr_normalized = autocorr_shifted / center_value
    else:
        autocorr_normalized = autocorr_shifted

    # Log transformation
    log_autocorr = torch.log1p(10 * torch.abs(autocorr_normalized) + epsilon)

    # Convert back to NumPy
    return log_autocorr.cpu().numpy()
