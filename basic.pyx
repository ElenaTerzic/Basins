#!/usr/bin/env cython

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import numpy as np
cimport numpy as np

from libcpp cimport bool

# Declare the class with cdef
cdef extern from "geometry.h" namespace "Geom":
	# Point class
	cdef cppclass CPoint "Geom::Point":
		CPoint() except +
		CPoint(const double, const double, const double) except +
		void    set(const int i, const double val)
		void    set(const double *v)
		double  get(const int i)
		double  x()
		double  y()
		double  z()
		double  dist(const CPoint &pp) const
		double  dist2(const CPoint &pp) const
		double isLeft(const CPoint &P0, const CPoint &P1) const
	# Vector class
	cdef cppclass CVector "Geom::Vector":
		CVector() except +
		CVector(const double x, const double y, const double z) except +
		CVector(const double *p) except +
		void    set(const int i, const double val)
		void    set(const double *p)
		double  get(const int i)
		double  x()
		double  y()
		double  z()
		double  dot(const CVector &vv) const
		CVector cross(const CVector &vv) const
		double  norm() const
		double  norm2() const
	# Ball class
	cdef cppclass CBall "Geom::Ball":
		CBall() except +
		CBall(const double r, const CPoint &p) except +
		CBall(const CPoint &p, const double r) except +
		CBall(const CPolygon &p) except +
		CPoint get_center() const
		double get_radius() const
		bool isempty() const
		bool isinside(const CPoint &p) const
		bool isdisjoint(const CBall &b) const
	# Polygon class
	cdef cppclass CPolygon "Geom::Polygon":
		CPolygon() except +
		CPolygon(const int nn) except +
		CPolygon(const int nn, const CPoint &v) except +
		CPolygon(const int nn, const CPoint *v) except +
		void    set_npoints(const int nn)
		void    set_point(const int i, const CPoint &v)
		void    set_points(const CPoint v)
		void    set_points(const CPoint *v)
		void    set_bbox(CBall &b)
		void    clear()
		void    set(const int nn, const CPoint &v)
		void    set(const int nn, const CPoint *v)
		CPoint *get_points() const
		CPoint  get_point(const int i) const
		int     get_npoints() const
		CBall   get_bbox() const
		bool    isempty() const
		bool    isinside(const CPoint &v) const
		bool    isinside_cn(const CPoint &v) const
		bool    isinside_wn(const CPoint &v) const


# Class wrapping a point
cdef class Point:
	'''
	A simple 3D point.
	'''
	cdef CPoint _point
	def __init__(self,double x, double y, double z):
		self._point = CPoint(x,y,z)

	def __str__(self):
		return '[ %f %f %f ]' % (self.x,self.y,self.z)

	# Operators
	def __getitem__(self,int i):
		'''
		Point[i]
		'''
		return self._point.get(i)

	def __setitem__(self,int i,double value):
		'''
		Point[i] = value
		'''
		self._point.set(i,value)

	def __add__(self,Vector other):
		'''
		Point = Point + Vector
		'''
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

	def __eq__(self,Point other):
		'''
		Point == Point
		'''
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

	def __ne__(self,Point other):
		'''
		Point != Point
		'''
		return not self == other

	# Functions
	def dist(self,Point p):
		'''
		Distance between two points
		'''
		return self._point.dist(p._point)

	def dist2(self,Point p):
		'''
		Distance between two points squared
		'''
		return self._point.dist2(p._point)

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
		cdef double out = self._point.isLeft(p1._point,p2._point)
		return out

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
		cdef double x1 = p1.x, x2 = p2.x, y1 = p1.y, y2 = p2.y
		cdef np.ndarray[np.double_t,ndim=1] out = np.ndarray((npoints,),dtype=np.double)
		for ii in range(npoints):
			out[ii] = ( (x2 - x1)*(xyz[ii,1] - y1) - (xyz[ii,0] - x1)*(y2 - y1) )
		return out

	@classmethod
	def from_array(cls,double[:] xyz):
		'''
		Build a point from an xyz array of shape (3,)
		'''
		return cls(xyz[0],xyz[1],xyz[2])

	@property
	def x(self):
		return self._point.x()
	@property
	def y(self):
		return self._point.y()
	@property
	def z(self):
		return self._point.z()
	@property
	def xyz(self):
		cdef np.ndarray[np.double_t,ndim=1] _xyz = np.ndarray((3,),dtype=np.double)
		_xyz[0] = self._point.x()
		_xyz[1] = self._point.y()
		_xyz[2] = self._point.z()
		return _xyz
	@xyz.setter
	def xyz(self,double[:] value):
		self._point.set(&value[0])


# Class wrapping a vector
cdef class Vector:
	'''
	A simple 3D vector.
	'''
	cdef CVector _vector
	def __init__(self, double x, double y, double z):
		self._vector = CVector(x,y,z)

	def __str__(self):
		return '( %f %f %f )' % (self.x,self.y,self.z)

	# Operators
	def __getitem__(self,int i):
		'''
		Point[i]
		'''
		return self._vector.get(i)

	def __setitem__(self,int i,double value):
		'''
		Point[i] = value
		'''
		self._vector.set(i,value)

	def __add__(self,Vector other):
		'''
		Vector = Vector + Vector
		'''
		return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

	def __sub__(self,Vector other):
		'''
		Vector = Vector - Vector
		'''
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

	def __truediv__(self,double other):
		'''
		Vector = Vector/val
		'''
		return Vector(self.x/other,self.y/other,self.z/other)

	def __eq__(self,Vector other):
		'''
		Vector == Vector
		'''
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

	def __ne__(self,Vector other):
		'''
		Vector != Vector
		'''
		return not self == other

	# Functions
	def dot(self,Vector v):
		'''
		Dot product
		'''
		cdef double out = self._vector.dot(v._vector)
		return out
	
	def cross(self,Vector v):
		'''
		Cross product
		'''
		cdef Vector out = Vector(0.,0.,0.)
		out._vector = self._vector.cross(v._vector)
		return out

	def norm(self):
		'''
		Vector norm
		'''
		cdef double out = self._vector.norm()
		return out

	def norm2(self):
		'''
		Vector norm squared
		'''
		cdef double out = self._vector.norm2()
		return out

	@property
	def x(self):
		return self._vector.x()
	@property
	def y(self):
		return self._vector.y()
	@property
	def z(self):
		return self._vector.z()
	@property
	def xyz(self):
		cdef np.ndarray[np.double_t,ndim=1] _xyz = np.ndarray((3,),dtype=np.double)
		_xyz[0] = self._vector.x()
		_xyz[1] = self._vector.y()
		_xyz[2] = self._vector.z()
		return _xyz
	@xyz.setter
	def xyz(self,double[:] value):
		self._vector.set(&value[0])


# Class wrapping a ball
cdef class Ball:
	'''
	A 2D circle or a 3D sphere wrapped in a single class
	'''
	cdef CBall _ball
	def __init__(self, Point center = Point(0.,0.,0.), double radius = 0.):
		self._ball = CBall(center._point,radius)

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
		cdef bool out = self._ball.isempty()
		return out
	
	def isinside(self,Point point):
		cdef bool out = self._ball.isinside(point._point)
		return out

	def areinside(self,double[:,:] xyz):
		cdef int ii, npoints = xyz.shape[0]
		cdef CPoint p
		cdef np.ndarray[np.npy_bool,ndim=1,cast=True] out = np.ndarray((npoints,),dtype=np.bool)
		for ii in range(npoints):
			p       = CPoint(xyz[ii,0],xyz[ii,1],xyz[ii,2])
			out[ii] = self._ball.isinside(p)
		return out

	def isdisjoint(self,Ball ball):
		cdef bool out = self._ball.isdisjoint(ball._ball)
		return out

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
		cdef Ball out = cls(Point(0.,0.,0.),0.)
		out._ball = CBall(poly._poly)
		return out

	@property
	def center(self):
		cdef Point out = Point(0.,0.,0.)
		out._point = self._ball.get_center()
		return out
	@property
	def radius(self):
		cdef double out = self._ball.get_radius()
		return out

# Wrapper class for polygon
cdef class Polygon:
		'''
		A polygon set as an array of points. Can be either 2D or 3D.
		'''
		cdef CPolygon _poly
		cdef Point[:] _points
		def __init__(self,Point[:] points):
			cdef int ip, npoints = points.shape[0]
			self._poly.set_npoints(npoints) # Already allocates npoints + 1!
			self._points = points
			for ip in range(npoints):
				self._poly.set_point(ip,points[ip]._point)
			self._poly.set_point(npoints,points[0]._point)
			# Set boundig box
			cdef CBall bbox = CBall(self._poly)
			self._poly.set_bbox(bbox)

		def __dealloc__(self):
			self._poly.clear()

		def __str__(self):
			cdef int ip = 0
			cdef object retstr = 'Point %d %s' % (ip,self.points[ip].__str__())
			for ip in range(1,self.npoints):
				retstr += '\nPoint %d %s' % (ip,self.points[ip].__str__())
			return retstr

		# Operators
		def __getitem__(self,int i):
			'''
			Polygon[i]
			'''
			cdef Point out = Point(0.,0.,0.)
			out._point = self._poly.get_point(i)
			return out

		def __setitem__(self,int i,Point value):
			'''
			Polygon[i] = value
			'''
			self._poly.set_point(i,value._point)

		def __eq__(self,Polygon other):
			'''
			Polygon == Polygon
			'''
			cdef int ip, np1= self.npoints, np2 = other.npoints
			# Check if polygons have the same number of points
			if not np1 == np2:
				return False
			# Check if the points are equal
			for ip in range(np1):
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
			cdef bool out = self._poly.isempty()
			return out

		def isinside(self,Point point):
			'''
			Returns True if the point is inside the polygon, else False.
			'''
			cdef bool out = self._poly.isinside(point._point)
#			cdef bool out =  self._poly.isinside_cn(point._point)
#			cdef bool out =  self._poly.isinside_wn(point._point)
			return out

		def areinside(self,double[:,:] xyz):
			'''
			Returns True if the points are inside the polygon, else False.
			'''
			cdef int ii, npoints = xyz.shape[0]
			cdef CPoint p
			cdef np.ndarray[np.npy_bool,ndim=1,cast=True] out = np.ndarray((npoints,),dtype=np.bool)
			for ii in range(npoints):
				p       = CPoint(xyz[ii,0],xyz[ii,1],xyz[ii,2])
				out[ii] = self._poly.isinside(p)
			return out

		@classmethod
		def from_array(cls,double[:,:] xyz):
			'''
			Build a polygon from an array of points
			of shape (npoints,3).
			'''
			cdef int ii, npoints = xyz.shape[0]
			pointList = np.array([Point.from_array(xyz[ii,:]) for ii in range(npoints)],dtype=Point)
			return cls(pointList)

		@property
		def npoints(self):
			return self._poly.get_npoints() # Returns correctly
		@property
		def points(self):
			return self._points
		@points.setter
		def points(self,Point[:] value):
			cdef int ip
			cdef npoints = value.shape[0]
			self._poly.set_npoints(npoints) # Already allocates npoints + 1!
			self._points = value
			for ip in range(npoints):
				self._poly.set_point(ip,value[ip]._point)
			self._poly.set_point(npoints,value[0]._point)
		@property
		def bbox(self):
			cdef Ball out = Ball()
			out._ball = self._poly.get_bbox()
			return out
		@bbox.setter
		def bbox(self,Ball value):
			self._poly.set_bbox(value._ball)
		@property
		def x(self):
			cdef int ii, npoints = self.npoints+1
			cdef np.ndarray[np.double_t,ndim=1] out = np.ndarray((npoints,),dtype=np.double)
			for ii in range(npoints):
				out[ii] = self._poly.get_point(ii).x()
			return out
		@property
		def y(self):
			cdef int ii, npoints = self.npoints+1
			cdef np.ndarray[np.double_t,ndim=1] out = np.ndarray((npoints,),dtype=np.double)
			for ii in range(npoints):
				out[ii] = self._poly.get_point(ii).y()
			return out
		@property
		def z(self):
			cdef int ii, npoints = self.npoints+1
			cdef np.ndarray[np.double_t,ndim=1] out = np.ndarray((npoints,),dtype=np.double)
			for ii in range(npoints):
				out[ii] = self._poly.get_point(ii).z()
			return out