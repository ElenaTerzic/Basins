#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import shapefile
import Basins

FILENAME = '/home/arnaumiro/projects/DATA/ShapeFiles/WorldSeas_v3/World_Seas_IHO_v3'

sf  = shapefile.Reader(FILENAME)

# Loop every lake
for idx in range(len(sf)):
	rec = sf.record(idx)
	if 'Adriatic' in rec[0]: print(idx,rec[0])

# Extract Kotor bay
print(sf.record(41))
shp = sf.shape(41)
xy_orig  = np.array(shp.points)
rect = Basins.SimpleRectangle(18.45,18.8,42.30,42.60)
mask = rect.areinside(xy_orig)
xy = xy_orig[mask]
plt.plot(xy[:,0],xy[:,1],'.k')

# Detect jump
d    = np.diff(xy,axis=0)
norm = np.sqrt(np.sum(d*d,axis=1))
ids  = np.where(norm > 0.1*np.max(norm))[0]
st   = ids[-2]-2
print(ids,st)
plt.plot(xy[14:st,0],xy[14:st,1],'k')

# Save data as xyz points
xyz = np.zeros((st-14,3),dtype=np.double)
xyz[:,0] = xy[14:st,0]
xyz[:,1] = xy[14:st,1]

np.save('../Basins/shapes/Kotor_WorldSeas.npy',xyz)

plt.show()