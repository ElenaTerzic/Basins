#!/usr/bin/env python

# Edited by amiro and eterzic 13.01.2022

from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

bornholm = Basin.from_array('born', 'Bornholm', np.array([[15, 54.5 , 0.],   [17.8, 54.5 , 0.], [17.8, 55.5 , 0.], [15, 55.5 , 0.]])) 
gdansk   = Basin.from_array('gdan', 'Gdansk'  , np.array([[18.1, 53.8, 0.],  [20., 53.8, 0.],   [20., 55.15, 0.],  [18.1, 53.8, 0.]])) 
gotland  = Basin.from_array('gotl', 'Gotland' , np.array([[18.1, 55.15, 0.], [22., 55.15, 0.],  [22., 60., 0.],    [18.1, 60., 0.]])) 

del print_function, division, os, np, Basin, ComposedBasin