#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import Basins

# Load  basin
basin = Basins.worldseas.med
print(basin)

# Plot
fig = plt.figure(1,(8,6),dpi=100)
ax  = fig.add_subplot(1,1,1)
for b in basin:
	plt.plot(b.x,b.y,'o-k')
plt.scatter(basin.centroid.x,basin.centroid.y,marker='x',c='k')

plt.show()