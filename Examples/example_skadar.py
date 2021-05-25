#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import Basins

# Load Skadar mid-res basin
basin = Basins.skadar_midres
print(basin)

# Check if some points are inside
xyzp = np.array([[19.45,42.30,0.],[19.3801,42.2972,0.],[19.23,42.24,0.],[19.2,42.1,0.]])
inside = basin.areinside(xyzp)

# Plot
plt.figure(1,(8,6),dpi=100)
plt.plot(basin.x,basin.y,'o-k')
plt.scatter(basin.centroid.x,basin.centroid.y,marker='x',c='k')
for ip in range(xyzp.shape[0]):
	print('p%d = '%ip,xyzp[ip,:],'inside' if inside[ip] else 'outside')
	plt.scatter(xyzp[ip,0],xyzp[ip,1],marker='x',c='b' if inside[ip] else 'r') # Blue if inside, red if outside

plt.show()