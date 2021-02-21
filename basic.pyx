#!/usr/bin/env cython
# cython: boundscheck=False
# cython: cdivision=True
# cython: wraparound=False
# cython: nonecheck=False

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
cimport numpy as np, cython

from libc.math cimport sqrt

cdef class Point:
	'''
	A simple 3D point.
	'''
	cdef double _xyz[3]
	def __init__(self,double x,double y ,double z):
		self._xyz[0] = x
		self._xyz[1] = y
		self._xyz[2] = z

	def __str__(self):
		return '[ %f %f %f ]' % (self.x,self.y,self.z)

	# Operators
	def __getitem__(self,int i):
		'''
		Point[i]
		'''
		return self._xyz[i]

	def __setitem__(self,int i,double value):
		'''
		Point[i] = value
		'''
		self._xyz[i] = value

	def __add__(self,object other):
		'''
		Point = Point + Vector
		'''
		if not isinstance(other,Vector):
			raise ValueError('Only Point + Vector is allowed!')
		return Point(self.x+other.x,self.y+other.y,self.z+other.z)

	def __sub__(self,object other):
		'''
		Point  = Point - Vector
		Vector = Point - Point
		'''
		if isinstance(other,Vector):
			return Point(self.x-other.x,self.y-other.y,self.z-other.z)
		if isinstance(other,Point):
			return Vector(self.x-other.x,self.y-other.y,self.z-other.z)
		raise ValueError('Unknown instance in Point subtraction!')

	def __eq__(self,object other):
		'''
		Point == Point
		'''
		if not isinstance(other,Point):
			raise ValueError('Only Point == Point is allowed!')
		return ( (self.x == other.x) and (self.y == other.y) and (self.z == other.z) )

	def __ne__(self,object other):
		'''
		Point != Point
		'''
		return not self == other

	# Functions
	def dist(self,Point p):
		'''
		Distance between two points
		'''
		cdef Vector v = self - p # Vector as the difference between two points
		return v.norm()

	def dist2(self,Point p):
		'''
		Distance between two points squared
		'''
		cdef Vector v = self - p # Vector as the difference between two points
		return v.norm2()

	def isLeft(self,Point p1,Point p2):
		'''
		ISLEFT

		Tests if a point is Left|On|Right of an infinite line.

		Input:  two points P1, P2; defining a line
		Return: >0 for P2 left of the line through P0 and P1
				=0 for P2  on the line
				<0 for P2  right of the line
		
		from: http://geomalgorithms.com/a03-_inclusion.html
		
		Copyright 2001 softSurfer, 2012 Dan Sunday
		This code may be freely used and modified for any purpose
		providing that this copyright notice is included with it.
		SoftSurfer makes no warranty for this code, and cannot be held
		liable for any real or imagined damage resulting from its use.
		Users of this code must verify correctness for their application.
		'''
		return ( (p2.x - p1.x)*(self.y - p1.y) - (self.x - p1.x)*(p2.y - p1.y) )

	@staticmethod
	def areLeft(double[:,:] xyz,Point p1,Point p2):
		'''
		ARELEFT

		Tests if a set of points are Left|On|Right of an infinite line.

		Input:  two points P1, P2; defining a line
		Return: >0 for P2 left of the line through P0 and P1
				=0 for P2  on the line
				<0 for P2  right of the line
		
		from: http://geomalgorithms.com/a03-_inclusion.html
		
		Copyright 2001 softSurfer, 2012 Dan Sunday
		This code may be freely used and modified for any purpose
		providing that this copyright notice is included with it.
		SoftSurfer makes no warranty for this code, and cannot be held
		liable for any real or imagined damage resulting from its use.
		Users of this code must verify correctness for their application.
		'''
		cdef int ii, npoints = xyz.shape[0]
		cdef np.ndarray[np.int_t,ndim=1] out = np.zeros((npoints,),dtype=np.int)
		for ii in range(npoints):
			out[ii] = ( (p2.x - p1.x)*(xyz[ii,1] - p1.y) - (xyz[ii,0] - p1.x)*(p2.y - p1.y) )
		return out

	@classmethod
	def from_array(cls,double[:] xyz):
		'''
		Build a point from an xyz array of shape (3,)
		'''
		return cls(xyz[0],xyz[1],xyz[2])

	@property
	def x(self):
		return self._xyz[0]
	@property
	def y(self):
		return self._xyz[1]
	@property
	def z(self):
		return self._xyz[2]
	@property
	def xyz(self):
		return self._xyz


cdef class Vector:
	'''
	A simple 3D vector.
	'''
	cdef double _xyz[3]
	def __init__(self, double x, double y, double z):
		self._xyz = np.array([x,y,z])

	def __str__(self):
		return '( %f %f %f )' % (self.x,self.y,self.z)

	# Operators
	def __getitem__(self,int i):
		'''
		Point[i]
		'''
		return self._xyz[i]

	def __setitem__(self,int i,double value):
		'''
		Point[i] = value
		'''
		self._xyz[i] = value

	def __add__(self,object other):
		'''
		Vector = Vector + Vector
		'''
		if not isinstance(other,Vector):
			raise ValueError('Only Vector + Vector is allowed!')
		return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

	def __sub__(self,object other):
		'''
		Vector = Vector - Vector
		'''
		if not isinstance(other,Vector):
			raise ValueError('Only Vector - Vector is allowed!')
		return Vector(self.x-other.x,self.y-other.y,self.z-other.z)

	def __mul__(self,object other):
		'''
		Vector = Vector*val
		val    = Vector*Vector
		'''
		if isinstance(other,Vector):
			return self.dot(other)
		else:
			return Vector(other*self.x,other*self.y,other*self.z)

	def __rmul__(self,object other):
		'''
		Vector = val*Vector
		val    = Vector*Vector
		'''
		return self.__mul__(other)

	def __truediv__(self,object other):
		'''
		Vector = Vector/val
		'''
		return Vector(self.x/other,self.y/other,self.z/other)

	def __eq__(self,object other):
		'''
		Vector == Vector
		'''
		if not isinstance(other,Vector):
			raise ValueError('Only Vector == Vector is allowed!')
		return ( (self.x == other.x) and (self.y == other.y) and (self.z == other.z) )

	def __ne__(self,object other):
		'''
		Vector != Vector
		'''
		return not self == other

	# Functions
	def dot(self,Vector v):
		'''
		Dot product
		'''
		return (self.x*v.x + self.y*v.y + self.z*v.z)
	
	def cross(self,Vector v):
		'''
		Cross product
		'''
		return Vector(self.y*v.z-self.z*v.y,-self.x*v.z+self.z*v.x,self.x*v.y-self.y*v.x)

	def norm(self):
		'''
		Vector norm
		'''
		return sqrt(self.norm2())

	def norm2(self):
		'''
		Vector norm squared
		'''
		return self.dot(self)

	@property
	def x(self):
		return self._xyz[0]
	@property
	def y(self):
		return self._xyz[1]
	@property
	def z(self):
		return self._xyz[2]
	@property
	def xyz(self):
		return self._xyz

cdef class Ball:
	'''
	A 2D circle or a 3D sphere wrapped in a single class
	'''
	cdef Point  _center
	cdef double _radius
	def __init__(self, Point center = Point(0.,0.,0.), double radius = 0.):
		self._center = center
		self._radius = radius

	def __str__(self):
		return 'center = ' + self.center.__str__() + ' radius = %f' % (self.radius)

	# Operators
	def __eq__(self,Ball other):
		'''
		Ball == Ball
		'''
		return self.center == other.center and self.radius == other.radius

	def __gt__(self,object other):
		'''
		self.isinside(other)
		'''
		if isinstance(other,Point):
			return self.isinside(other)
		else:
			return self.areinside(other)

	def __lt__(self,object other):
		'''
		not self.isinside(other)
		'''
		if isinstance(other,Point):
			return not self.isinside(other)
		else:
			return np.logical_not(self.areinside(other))

	# Functions
	def isempty(self):
		return self._radius == 0
	
	def isinside(self,Point point):
		return True if not self.isempty() and point.dist(self.center) < self.radius else False

	def areinside(self,double[:,:] xyz):
		cdef int ii, npoints = xyz.shape[0]
		cdef Point p
		cdef np.ndarray[np.npy_bool,ndim=1,cast=True] out = np.zeros((npoints,),dtype=np.bool)
		
		for ii in range(npoints):
			p = Point.from_array(xyz[ii,:])
			out[ii] = self.isinside(p)
		return out

	def isdisjoint(self,Ball ball):
		return True if not self.isempty() and ball.center.dist(self.center) < self.radius + ball.radius else False

	@classmethod
	def fastBall(cls,Polygon poly):
		'''
		FASTBALL

		Get a fast approximation for the 2D bounding ball 
		(based on the algorithm given by [Jack Ritter, 1990]).

		Input:  A polygon
		Output: Nothing, sets the ball class

		from: http://geomalgorithms.com/a08-_containers.html

		Copyright 2001 softSurfer, 2012 Dan Sunday
		This code may be freely used and modified for any purpose
		providing that this copyright notice is included with it.
		SoftSurfer makes no warranty for this code, and cannot be held
		liable for any real or imagined damage resulting from its use.
		Users of this code must verify correctness for their application.
		'''
		cdef int ii
		cdef double xmin, xmax, ymin, ymax  # bounding box extremes
		cdef int Pxmin, Pxmax, Pymin, Pymax # index of  P[] at box extreme

		# Find a large diameter to start with
		# first get the bounding box and P[] extreme points for it
		xmin = xmax = poly[0][0]
		ymin = ymax = poly[0][1]
		Pxmin = Pxmax = Pymin = Pymax = 0

		for ii in range(poly.npoints):
			if poly[ii][0] < xmin:
				xmin  = poly[ii][0]
				Pxmin = ii
			elif poly[ii][0] > xmax:
				xmax  = poly[ii][0]
				Pxmax = ii
			if poly[ii][1] < ymin:
				ymin  = poly[ii][1]
				Pymin = ii
			elif poly[ii][1] > ymax:
				ymax  = poly[ii][1]
				Pymax = ii

		# Select the largest extent as an initial diameter for the  ball
		cdef Point center = Point(0.,0.,0.)
		cdef Vector dPx = poly[Pxmax] - poly[Pxmin], dPy = poly[Pymax] - poly[Pymin]
		cdef double rad2, dx2 = dPx.norm2(), dy2 = dPy.norm2()

		if dx2 >= dy2: # x direction is largest extent
			center = poly[Pxmin] + (dPx/2.) 
			rad2   = poly[Pxmax].dist2(center)
		else:
			center = poly[Pymin] + (dPy/2.)
			rad2   = poly[Pymax].dist2(center)

		cdef double rad = sqrt(rad2)

		# Now check that all points p[i] are in the ball
		# and if not, expand the ball just enough to include them
		cdef Vector dP
		cdef double dist, dist2;

		for ii in range(poly.npoints):
			dP    = poly[ii] - center 
			dist2 = dP.norm2()
			if (dist2 <= rad2): continue # p[i] is inside the ball already
			# p[i] not in ball, so expand ball  to include it
			dist   = sqrt(dist2)
			rad    = (rad + dist)/2.
			rad2   = rad*rad # enlarge radius just enough
			center = center + dP*((dist-rad)/dist) # shift Center toward p[i]

		# Return the ball
		return cls(center,rad)

	@property
	def center(self):
		return self._center
	@property
	def radius(self):
		return self._radius


cdef class Polygon:
		'''
		A polygon set as an array of points. Can be either 2D or 3D.
		'''
		cdef int _npoints
		cdef np.ndarray _points
		cdef Ball _bbox
		def __init__(self, list points):
			cdef int ip
			self._npoints = len(points)
			# Copy points
			self._points = np.array([Point(p.x,p.y,p.z) for p in points],dtype=np.object)
			self._points = np.append(self._points,np.array(Point(points[0].x,points[0].y,points[0].z)))
			self._bbox   = Ball.fastBall(self) # Create a ball bounding box using fastBall

		def __str__(self):
			cdef int ip
			cdef object retstr = ''
			for ip in range(self.npoints):
				retstr += 'Point %d ' % ip + self._points[ip].__str__() + '\n'
			return retstr

		# Operators
		def __getitem__(self,int i):
			'''
			Polygon[i]
			'''
			return self._points[i]

		def __setitem__(self,int i,Point value):
			'''
			Polygon[i] = value
			'''
			self._points[i] = value

		def __eq__(self,Polygon other):
			'''
			Polygon == Polygon
			'''
			# Check if polygons have the same number of points
			if not self.npoints == other.npoints:
				return False
			# Check if the points are equal
			for ip in range(self.npoints):
				if not self[ip] == other[ip]:
					return False
			return True

		def __ne__(self,Polygon other):
			'''
			Polygon != Polygon
			'''
			return not self.__eq__(other)

		def __gt__(self,object other):
			'''
			self.isinside(other)
			'''
			if isinstance(other,Point):
				return self.isinside(other) # Return true if Point inside Polygon
			else: # Assume numpy array
				return self.areinside(other)

		def __lt__(self,object other):
			'''
			not self.isinside(other)
			'''
			if isinstance(other,Point):
				return not self.isinside(other)
			else:
				return np.logical_not(self.areinside(other))

		# Functions
		def isempty(self):
			return self.npoints == 0

		def isinside(self,Point point):
			'''
			Returns True if the point is inside the polygon, else False.
			'''
			if self.bbox > point: # Point is inside the bounding box
				# Select the algorithm to use
				#return True if wn_PinPoly(point,self) > 0  else False
				return True if cn_PinPoly(point,self) == 1 else False
			else:
				return False

		def areinside(self,double[:,:] xyz):
			'''
			Returns True if the points are inside the polygon, else False.
			'''
			cdef int ii, npoints = xyz.shape[0]
			cdef Point p
			cdef np.ndarray[np.npy_bool,ndim=1,cast=True] out = np.zeros((npoints,),dtype=np.bool)
			for ii in range(npoints):
				p = Point.from_array(xyz[ii,:])
				out[ii] = self.isinside(p)
			return out

		@classmethod
		def from_array(cls,double[:,:] xyz):
			'''
			Build a polygon from an array of points
			of shape (npoints,3).
			'''
			cdef int ii, npoints = xyz.shape[0]
			cdef list pointList = [Point.from_array(xyz[ii,:]) for ii in range(npoints)] 
			return cls(pointList)

		@property
		def npoints(self):
			return self._npoints
		@property
		def points(self):
			return self._points
		@property
		def bbox(self):
			return self._bbox
		@property
		def x(self):
			cdef int ii
			cdef np.ndarray[np.double_t,ndim=1] out = np.zeros((self._npoints,),dtype=np.double)
			for ii in range(self._npoints):
				out[ii] = self._points[ii].x
			return out
		@property
		def y(self):
			cdef int ii
			cdef np.ndarray[np.double_t,ndim=1] out = np.zeros((self._npoints,),dtype=np.double)
			for ii in range(self._npoints):
				out[ii] = self._points[ii].y
			return out
		@property
		def z(self):
			cdef int ii
			cdef np.ndarray[np.double_t,ndim=1] out = np.zeros((self._npoints,),dtype=np.double)
			for ii in range(self._npoints):
				out[ii] = self._points[ii].z
			return out


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.nonecheck(False)
def cn_PinPoly(Point point, Polygon poly):
	'''
	CN_PINPOLY

	2D algorithm.
	Crossing number test for a point in a polygon.

	Input:   P = a point,
	Return:  0 = outside, 1 = inside

	This code is patterned after [Franklin, 2000]
	from: http://geomalgorithms.com/a03-_inclusion.html

	Copyright 2001 softSurfer, 2012 Dan Sunday
	This code may be freely used and modified for any purpose
	providing that this copyright notice is included with it.
	SoftSurfer makes no warranty for this code, and cannot be held
	liable for any real or imagined damage resulting from its use.
	Users of this code must verify correctness for their application.
	'''
	cdef int ip, npoints = poly.npoints, cn = 0 # The crossing number counter
	cdef double vt
	# Loop through all edges of the Polygon
	for ip in range(npoints): 
		# an upward crossing or a downward crossing
		if ( (poly[ip][1] <= point[1]) and (poly[ip+1][1] >  point[1]) ) or \
		   ( (poly[ip][1] >  point[1]) and (poly[ip+1][1] <= point[1]) ):
			# Compute  the actual edge-ray intersect x-coordinate
			vt = (point[1] - poly[ip][1])/(poly[ip+1][1] - poly[ip][1])
					
			if point[0] <  poly[ip][0] + vt * (poly[ip+1][0] - poly[ip][0]): # P.x < intersect
				cn += 1 # A valid crossing of y=P.y right of P.x
	return not cn%2 == 0 # 0 if even (out), and 1 if  odd (in)