# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:23:48 2024

@author: ardag
"""
import numpy as np
import matplotlib.pyplot as plt


def BF(data, x, y, map_i, map_j, mask=2):
    aveDP = data[1, 1, :, :]
    
    
    
    ## Create BF image
    # create mask
    ic = x
    jc = y
    x,y = np.indices((aveDP.shape[0], aveDP.shape[1]))
    mask_BF = (x-ic) ** 2 + (y-jc)**2 < mask ** 2
    
    # plot mask to check alignment
    fig, ax = plt.subplots(ncols=3, figsize=(8,3))
    ax[0].imshow(aveDP, cmap='gray')
    ax[1].imshow(mask_BF, cmap='plasma')
    
    ax[2].imshow(aveDP, cmap='magma')
    ax[2].imshow(mask_BF, cmap='gray', alpha=0.5)
    
    ax[0].set_title('CBED')
    ax[1].set_title('mask')
    ax[2].set_title('overlay')
    plt.show()
    
    
    # initalize BF image creating an empty array
    BF = np.zeros((map_i, map_j))
    
    # integrate diffractin space to create BF image
    
    for i in range(0, int(aveDP.shape[0])):
       for j in range(0, int(aveDP.shape[1])):
          if mask_BF[i,j]:
             BF = BF+data[:, :, i,j]
    # plot BF image
    fig,ax=plt.subplots()
    ax.imshow(BF, cmap=plt.cm.gray)
    plt.show()
    
    return BF
    
    
