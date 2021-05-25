#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import shapefile

# Read HydroLAKES DB
sf  = shapefile.Reader("HydroLAKES_polys_v10")

# Loop every lake
#for idx in range(len(sf)):
#	skip = True
#	try:
#		rec = sf.record(idx)
#
#		if 'skadar' in rec[1].lower(): skip = False 
#		if rec[2] == 'Montenegro':     skip = False
#		if rec[2] == 'Albania':        skip = False
#			
#		if skip: continue
#		
#		print(rec)                                                                 
#	except:
#		print('Cannot read recording',idx)
#
#	shp = sf.shape(idx)
#	xy  = np.array(shp.points)
#	plt.plot(xy[:,0],xy[:,1],'.k')
#	plt.show()

idx = 1302 # Record #1302: [1303, 'Scutari', 'Albania', 'Europe', 'SWBD', 1, 0, 380.69, 207.38, 3.0, 15558.26, 0.0, 3, 40.9, 167.386, 1075.8, 1, 4.84, 3883.7, 19.491171, 42.052998]

rec = sf.record(idx)
print(rec)                                                                 
shp = sf.shape(idx)
xy  = np.array(shp.points)
plt.plot(xy[:,0],xy[:,1],'.k')

# Detect jump
d    = np.diff(xy,axis=0)
norm = np.sqrt(np.sum(d*d,axis=1))
ids  = np.where(norm > 100.*np.min(norm))[0]
print(ids)

# Save Skadar lake as xyz points
xyz = np.zeros((980,3),dtype=np.double)
xyz[:,0] = xy[:980,0]
xyz[:,1] = xy[:980,1]

np.save('../Basins/shapes/Skadar_HydroLAKES.npy',xyz)

plt.plot(xy[:980:6,0],xy[:980:6,1],'k')
print(xy[:980:6,:].shape)
plt.show()