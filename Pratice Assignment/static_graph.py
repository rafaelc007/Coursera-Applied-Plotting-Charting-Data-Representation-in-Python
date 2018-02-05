# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:40:26 2018

@author: rafael
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def plot_standard(ax):
    '''Standard way to plot the histograms providade by coursera'''
    # plot the histograms
    names = ['x1\nNormal', 'x2\nGamma', 'x3\nExponential', 'x4\nUniform']
    plt.figure(figsize=(9,3))
    for axis in ax:
        plt.hist(axis, normed=True, bins=20, alpha=0.5);
    
    plt.axis([-7,21,0,0.6])
    for ix in range(len(names)):
        plt.text(ax[ix].mean()-1.5, 0.5, names[ix])
    
def plot_subplots(ax):
    colors = ['blue', 'green', 'red', 'cyan']
    fig, axes = plt.subplots(2, 2, sharey = True)
    for i in range(4):
        axes[int(i>=2), i%2].hist(ax[i], normed=True, bins=20, alpha=0.5, color = colors[i]);
            
if name == "__init__":
    x1 = np.random.normal(-2.5, 1, 10000)
    x2 = np.random.gamma(2, 1.5, 10000)
    x3 = np.random.exponential(2, 10000)+7
    x4 = np.random.uniform(14,20, 10000)

    plot_subplots([x1,x2,x3,x4])
