#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import os, numpy as np
import matplotlib.pyplot as plt

import Basins
SHAPESPATH = Basins.worldseas.SHAPESPATH


# Recover adriatic basin
adr = Basins.Basin.from_npy('adr', 'Adriatic Sea', os.path.join(SHAPESPATH,'Adriatic_WorldSeas.npy'),downsample=1)

# Recover the points
xyz = np.array([p.xyz for p in adr.points])
print(xyz)

# Generate a polygon for North Adriatic
n_adr = Basins.Polygon.from_array(np.array([[13.4088134765625, 43.620170616189895, 0.],[15.238037109375, 44.12308489306967,  0.],[15.924682617187498, 44.43377984606822,  0.],[13.886718749999998, 46.195042108660154, 0.],[11.25, 45.38301927899065,  0.],[12.216796875, 43.929549935614595, 0.]]))
m_adr = Basins.Polygon.from_array(np.array([[17.720947265625,    43.04480541304369,  0.],[16.094970703125,    41.87774145109676,  0.],[14.886474609375,    41.82045509614034,  0.],[13.743896484375,    42.512601715736665, 0.],[13.4088134765625,   43.620170616189895, 0.],[15.238037109375,    44.12308489306967,  0.],[15.440039062499996, 44.15068115978094,  0.]]))
s_adr = Basins.Polygon.from_array(np.array([[19.698486328124996, 41.983994270935625, 0.],[17.720947265625,    43.04480541304369 , 0.],[16.094970703125,    41.87774145109676 , 0.],[15.57861328125,     41.43449030894922 , 0.],[17.314453125,       40.713955826286046, 0.],[17.99560546875,     40.3549167507906  , 0.],[18.355407714843746, 39.78954439311165 , 0.],[20.093994140624996, 39.78954439311165 , 0.]]))

# Select the points that are inside the North Adriatic
xyz_nadr = xyz[n_adr.areinside(xyz)]
xyz_madr = xyz[m_adr.areinside(xyz)]
xyz_sadr = xyz[s_adr.areinside(xyz)]

# Plot regions
plt.plot(xyz[:,0],xyz[:,1],'.k')
plt.plot(xyz_nadr[:,0],xyz_nadr[:,1],'k')
plt.plot(xyz_madr[:,0],xyz_madr[:,1],'b')
plt.plot(xyz_sadr[:,0],xyz_sadr[:,1],'r')

# Save as numpy array
np.save('../Basins/shapes/North_Adriatic.npy',xyz_nadr)
np.save('../Basins/shapes/Mid_Adriatic.npy',  xyz_madr)
np.save('../Basins/shapes/South_Adriatic.npy',xyz_sadr)

plt.show()