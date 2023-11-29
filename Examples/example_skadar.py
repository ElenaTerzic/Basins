#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import Basins

# Load Skadar basin
basin = Basins.hydrolakes.skadar_highres
print(basin)

# Check if some points are inside
lon  = np.array([19.45,19.3801,19.23,19.2])
lat  = np.array([42.30,42.2972,42.24,42.1])
xyzp = np.zeros((len(lon),3))
xyzp[:,0] = lon
xyzp[:,1] = lat
inside = basin.areinside(xyzp)

# Plot
plt.figure(1,(8,6),dpi=100)
plt.plot(basin.x,basin.y,'o-k')
plt.scatter(basin.centroid.x,basin.centroid.y,marker='x',c='k')
for ip in range(xyzp.shape[0]):
	print('p%d = '%ip,xyzp[ip,:],'inside' if inside[ip] else 'outside')
	plt.scatter(xyzp[ip,0],xyzp[ip,1],marker='x',c='b' if inside[ip] else 'r') # Blue if inside, red if outside

plt.show()