# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:20:06 2018

@author: rafael
Coursera Applied Python week 3
Practice Assignment: Understanding Distributions Through Sampling
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

x = [x1, x2, x3, x4]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey = True)

ax = [ax1, ax2, ax3, ax4]

axis1 = [-7.5, 2.5, 0, 0.6]
axis2 = [0, 10, 0, 0.6]
axis3 = [7, 17, 0, 0.6]
axis4 = [12, 22, 0, 0.6]
axis = [axis1, axis2, axis3, axis4]

bins1 = np.arange(-7.5, 2.5, 0.2)
bins2 = np.arange(0, 10, 0.2)
bins3 = np.arange(7, 17, 0.2)
bins4 = np.arange(12, 22, 0.2)
bins = [bins1, bins2, bins3, bins4]

titles = ['x1 Normal', 'x2 Gamma', 'x3 Exponential', 'Normed Frequency']

def update_subplot(curr):
    if curr == 100:
        a.event_source.stop()
    for i in range(len(ax)):
        ax[i].cla()
        ax[i].hist(x[i][:100*curr], normed = True, bins = bins[i])
        ax[i].axis(axis[i])
        ax[i].set_title(titles[i])
        ax[i].set_ylabel('Normed Frequency')
        ax[i].set_xlabel('Value')
    plt.tight_layout()

a = animation.FuncAnimation(fig, update_subplot, interval = 100, repeat = True)
