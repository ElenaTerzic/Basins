#!/usr/bin/env python

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import Basins


xyz  = np.array([[0.,0. ,0.],[.5,.25,0.],[1.,0.,0.],[.7,1.,0.],[0.,1.,0.]])
poly = Basins.Polygon.from_array(xyz)
print(poly)

# Check if a point is inside
p1 = Basins.Point(.5,.5,0.)
p2 = Basins.Point(.35,.15,0.)

print( 'p1 = ', p1, 'inside' if poly > p1 else 'outside' )
print( 'p2 = ', p2, 'inside' if poly > p2 else 'outside' )


plt.figure(1,(8,6),dpi=100)
plt.plot(poly.x,poly.y,'o-k')
plt.scatter(p1.x,p1.y,marker='x',c='r' if poly < p1 else 'b') # Blue if inside, red if outside
plt.scatter(p2.x,p2.y,marker='x',c='r' if poly < p2 else 'b') # Blue if inside, red if outside

# Check if an array of points are inside
xyzp = np.array([[.5,.5,0.],[1.,.35,0.],[0.2,0.5,0.],[.35,.15,0.]])
inside = poly > xyzp

plt.figure(2,(8,6),dpi=100)
plt.plot(poly.x,poly.y,'o-k')

for ip in range(xyzp.shape[0]):
	print('p%d = '%ip,xyzp[ip,:],'inside' if inside[ip] else 'outside')
	plt.scatter(xyzp[ip,0],xyzp[ip,1],marker='x',c='b' if inside[ip] else 'r') # Blue if inside, red if outside

plt.show()