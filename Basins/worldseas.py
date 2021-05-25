#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# World Seas shapefile
adr    = Basin.from_npy('adr', 'Adriatic Sea'  , os.path.join(SHAPESPATH,'Adriatic_WorldSeas.npy'),downsample=4)
alb    = Basin.from_npy('alb', 'Alboran Sea'   , os.path.join(SHAPESPATH,'Alboran_WorldSeas.npy'),downsample=4)

socean = Basin.from_npy('so' , 'Southern Ocean', os.path.join(SHAPESPATH,'SouthernOcean_WorldSeas.npy'),downsample=4)

# Composed basins
