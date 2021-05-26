#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import shapefile
import Basins

FILENAME = '/home/arnaumiro/projects/DATA/ShapeFiles/WorldSeas_v3/World_Seas_IHO_v3'

sf  = shapefile.Reader(FILENAME)

# Loop every record
for idx in range(len(sf)):
	rec = sf.record(idx)
	if 'South Pacific' in rec[0]: print(idx,rec[0])

# Extract South Pacific Ocean
print(sf.record(63))
shp = sf.shape(63)
xy_orig = np.array(shp.points)

# Extract the region of positive longitudes
rect = Basins.SimpleRectangle(130.,181.,-70.,1.)
mask = rect.areinside(xy_orig)
xy   = xy_orig[mask]
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

np.save('../Basins/shapes/SouthPacific1_WorldSeas.npy',xyz)

# Extract the region of negative longitudes
rect = Basins.SimpleRectangle(-181.,0.,-70.,1.)
mask = rect.areinside(xy_orig)
rect = Basins.SimpleRectangle(-170.,-90,-30.,-12.)
mask1= ~rect.areinside(xy_orig)
xy   = xy_orig[np.logical_and(mask,mask1)]
plt.plot(xy[:,0],xy[:,1],'.k')

# Detect jump
d    = np.diff(xy,axis=0)
norm = np.sqrt(np.sum(d*d,axis=1))
ids  = np.where(norm > 0.03*np.max(norm))[0]
st   = ids[0]+1
print(ids,xy.shape,st)
plt.plot(xy[:st,0],xy[:st,1],'k')

# Save data as xyz points
xyz = np.zeros((st,3),dtype=np.double)
xyz[:,0] = xy[:st,0]
xyz[:,1] = xy[:st,1]

np.save('../Basins/shapes/SouthPacific2_WorldSeas.npy',xyz)

plt.show()