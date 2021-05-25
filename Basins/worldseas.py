#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# World Seas shapefile
adr    = Basin.from_npy('adr' , 'Adriatic Sea' , os.path.join(SHAPESPATH,'Adriatic_WorldSeas.npy'),downsample=4)
alb    = Basin.from_npy('alb' , 'Alboran Sea'  , os.path.join(SHAPESPATH,'Alboran_WorldSeas.npy'),downsample=4)
bal    = Basin.from_npy('bal' , 'Iberian Sea'  , os.path.join(SHAPESPATH,'Balearic_WorldSeas.npy'),downsample=4)
lig    = Basin.from_npy('lig' , 'Ligurian Sea' , os.path.join(SHAPESPATH,'Ligurian_WorldSeas.npy'),downsample=4)
west   = Basin.from_npy('west', 'Western Basin', os.path.join(SHAPESPATH,'WestMed_WorldSeas.npy'),downsample=4)

socean = Basin.from_npy('so' , 'Southern Ocean', os.path.join(SHAPESPATH,'SouthernOcean_WorldSeas.npy'),downsample=4)

# Composed basins
wmed   = ComposedBasin('wmed', 'Western Mediterranean', [alb,west,bal,lig])
