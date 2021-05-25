#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

__VERSION__ = 1.0

from .basic    import Point, Ball, Polygon
from .basins   import med, wmed, emed, socean
from .basins   import adr 
from .basins   import skadar_lowres, skadar_midres, skadar_highres, kotor
from .entities import Basin, ComposedBasin, Line, SimpleRectangle, Rectangle, Plane, SimpleCube, Cube

del basic, basins, entities