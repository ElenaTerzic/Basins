#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import shapefile

FILENAME = '/home/arnaumiro/projects/DATA/ShapeFiles/WorldSeas_v3/World_Seas_IHO_v3'

sf  = shapefile.Reader(FILENAME)

# Loop every lake
for idx in range(len(sf)):
	rec = sf.record(idx)
	if 'Baltic Sea' in rec[0]: print(idx,rec[0])

# Extract Baltic Sea
print(sf.record(56))
shp = sf.shape(56)
xy  = np.array(shp.points)
plt.plot(xy[:,0],xy[:,1],'.k')

# Detect jump
d    = np.diff(xy,axis=0)
norm = np.sqrt(np.sum(d*d,axis=1))
ids  = np.where(norm > 0.03*np.max(norm))[0]
st   = ids[0]+1
print(ids,st)
plt.plot(xy[:st,0],xy[:st,1],'k')

# Save data as xyz points
xyz = np.zeros((st,3),dtype=np.double)
xyz[:,0] = xy[:st,0]
xyz[:,1] = xy[:st,1]

np.save('../Basins/shapes/BalticSea_WorldSeas.npy',xyz)

plt.show()