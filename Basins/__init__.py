#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

__version__ = '1.6.7'

from .basic    import Point, Ball, Polygon
from .entities import Line, SimpleRectangle, Rectangle, Plane, SimpleCube, Cube, ConvexHull2D as ConvexHull
from .entities import Basin, Basin3D, ComposedBasin
from .         import generic, climate, hydrolakes, worldseas, worldcountries, adriatic, baltic, mediterranean

del basic, entities