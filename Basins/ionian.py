#!/usr/bin/env python

# Edited by eterzic 17.02.2025


from __future__ import print_function, division

import os, numpy as np

from .entities import Basin, ComposedBasin

# Path to the shapes directory
SHAPESPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'shapes')

# skip ion1

#ion1  = Basin.from_array('ion1' , 'Western Ionian'  , np.array([[9.25, 32.0,  0.],[15.0, 32.0,  0.],[15.0, 36.75, 0.],[10.7, 36.75, 0.],[9.25, 35.0 , 0.]]))
#ion2 = Basin.from_array('ion2' , 'Eastern Ionian'   , np.array([[15.0 , 30.0 , 0.],[21.85, 30.0 , 0.],[21.85, 36.75, 0.],[15.0 , 36.75, 0.]]) )
#ion3 = Basin.from_array('ion3' , 'Northern Ionian'  , np.array([[15.0 , 36.75, 0.],[21.85, 36.75, 0.],[21.85, 40.0 , 0.],[18.5 , 40.0 , 0.],[17.0 , 41.0 , 0.],[16.1 , 40.0 , 0.],[16.5 , 39.5 , 0.],[16.1 , 38.2 , 0.],[15.6 , 38.2 , 0.],[15.0 , 38.0 , 0.]]))


ionNW = Basin.from_array('ionNW' , 'North-western Ionian' , np.array([[17, 40.5 , 0],[19, 40., 0], [17.26, 36.6,  0],[15   , 36.6, 0]]))
ionNC = Basin.from_array('ionN'  , 'North-central Ionian' , np.array([[19, 40.  , 0],[19, 40., 0], [17.26, 36.6,  0],[19.53, 36.6, 0]]))
ionNE = Basin.from_array('ionNE' , 'North-eastern Ionian' , np.array([[19, 40.  , 0],[19, 40., 0], [19.53, 36.6,  0],[21.8 , 36.6, 0]]))

ionSW = Basin.from_array('ionSW' , 'South-western Ionian' , np.array([[15   , 36.6 , 0] ,[17.26, 36.6, 0] , [17.26, 30.0,  0],[15., 30.0, 0]]))
ionSC = Basin.from_array('ionS'  , 'South-central Ionian' , np.array([[17.26, 36.6 , 0] ,[19.53, 36.6, 0] , [19.53, 30.0,  0],[17.26, 30.0, 0]]))
ionSE = Basin.from_array('ionSE' , 'South-eastern Ionian' , np.array([[19.53, 36.6 , 0] ,[21.8 , 36.6, 0] , [21.8 , 30.0,  0],[19.53 , 30.0, 0]]))


# Composed basins
north = ComposedBasin('Nion', 'Northern Ionian', [ionNE,ionNC,ionNW])
south = ComposedBasin('Sion', 'Southern Ionian', [ionSE,ionSC,ionSW])

ionian = ComposedBasin('ion', 'Ionian', [ionNE,ionNC,ionNW, ionSE,ionSC,ionSW])

del print_function, division, os, np, Basin, ComposedBasin