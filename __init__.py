#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

__VERSION__ = 1.0

from .basic    import Point, Polygon
from .basins   import med, wmed, emed, socean, skadar, kotor 
from .entities import SimpleRectangle, Rectangle, Basin

del basic, basins, entities