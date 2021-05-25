#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# Basins definition
med    = Basin.from_array('med'  , 'Mediterranean Sea'    , np.array([[-5.71, 36.10 , 0.],[3.16 , 45.03 , 0.],[15.56, 46.98 , 0.],[28.39, 41.24 , 0.],[33.49, 40.45 , 0.],[37.53, 36.32 , 0.],[35.77, 30.75 , 0.],[29.79, 30.22 , 0.],[19.25, 29.38 , 0.],[-3.78, 33.94 , 0.],[-5.54, 34.45 , 0.]]))
wmed   = Basin.from_array('wmed' , 'Western Mediterranean', np.array([[-5.80, 36.14,0.],[ 4.00, 44.50,0.],[11.69, 44.56,0.],[16.88, 39.02,0.],[14.50, 37.75,0.],[14.94, 36.70,0.],[15.07, 32.10,0.],[-5.67, 34.89,0.]]))
emed   = Basin.from_array('emed' , 'Eastern Mediterranean', np.array([[15.12, 36.91, 0.],[15.07, 32.29, 0.],[17.49, 30.07, 0.],[21.97, 30.60, 0.],[37.88, 30.07, 0.],[36.91, 37.23, 0.],[31.82, 40.38, 0.],[29.27, 41.05, 0.],[25.22, 42.03, 0.],[19.51, 43.77, 0.],[15.82, 45.71, 0.],[13.62, 45.77, 0.],[12.30, 45.64, 0.],[11.51, 45.21, 0.]]))
socean = Basin.from_array('so'   , 'Southern Ocean'       , np.array([[60.64, -47.52 , 0.],[79.01, -47.28 , 0.],[78.50, -57.61 , 0.],[61.70, -56.80 , 0.]]) )
kotor  = Basin.from_array('kotor', 'Bay of Kotor'         , np.array([[18.48, 42.51, 0.],[18.48, 42.43, 0.],[18.52, 42.40, 0.],[18.58, 42.39, 0.],[18.78, 42.39, 0.],[18.78, 42.49, 0.],[18.69, 42.52, 0.]]))

# Skadar lake, shapefile from HydroLAKES
skadar_lowres  = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=6)
skadar_midres  = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=4)
skadar_highres = Basin.from_npy('skadar', 'Skadar Lake', os.path.join(SHAPESPATH,'Skadar_HydroLAKES.npy'),downsample=1)

# World Seas shapefile
adr    = Basin.from_npy('adr', 'Adriatic'      , os.path.join(SHAPESPATH,'Adriatic_WorldSeas.npy'),downsample=4)
socean = Basin.from_npy('so' , 'Southern Ocean', os.path.join(SHAPESPATH,'SouthernOcean_WorldSeas.npy'),downsample=4)
