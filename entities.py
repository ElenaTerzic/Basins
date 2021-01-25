#!/usr/bin/env python

# Edited by amiro and eterzic 25.01.2021

from __future__ import print_function, division

import numpy as np

from .basic import Point, Ball, Polygon


class Basin(Polygon):
	"""docstring for Basin"""
	def __init__(self,abbrev,name,points):
		super(Basin, self).__init__(points)
		self._abbrev = abbrev
		self._name   = name

	@classmethod
	def from_array(cls,abbrev,name,xyz):
		'''
		Build a basin from an array of points
		of shape (npoints,3).
		'''
		pointList = [Point.from_array(xyz[ii,:]) for ii in range(xyz.shape[0])] 
		return cls(abbrev,name,pointList)

	@property
	def abbrev(self):
		return self._abbrev

	@property
	def name(self):
		return self._name
	
		

class SimpleRectangle(Polygon):
	'''
	2D rectangle. Assumes z = 0 and the points aligned with the axis.
	For any other shape please use Rectangle or Polygon.

	4-------3
	|		|
	|		|
	1-------2
	'''
	def __init__(self,xmin,xmax,ymin,ymax):
		pointList = [
			Point(xmin,ymin,0.), # 1
			Point(xmax,ymin,0.), # 2
			Point(xmax,ymax,0.), # 3
			Point(xmin,ymax,0.), # 4
		]
		super(SimpleRectangle, self).__init__(pointList)

	def isinside(self,point,algorithm=None):
		'''
		A fast algorithm for simple rectangles.
		'''
		x_inside = point[0] >= self.points[0][0] and point[0] <= self.points[1][0]
		y_inside = point[1] >= self.points[0][1] and point[0] <= self.points[3][1]
		return x_inside and y_inside

	def areinside(self,xyz,algorithm=None):
		'''
		A fast algorithm for simple rectangles.
		'''
		x_inside = np.logical_and(xyz[:,0] >= self.points[0][0],xyz[:,0] <= self.points[1][0])
		y_inside = np.logical_and(xyz[:,1] >= self.points[0][1],xyz[:,1] <= self.points[3][1])
		return np.logical_and(x_inside,y_inside)

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a square from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 5: raise ValueError('Invalid number of points for Rectangle %d' % npoints)
		return super(SimpleRectangle, cls).from_array(xyz)


class Rectangle(Polygon):
	'''
	2D rectangle. Assumes z = 0.

	4-------3
	|		|
	|		|
	1-------2
	'''
	def __init__(self,points):
		if not len(points) == 4: raise ValueError('Invalid Rectangle!')
		super(Rectangle, self).__init__(points)

	def normal(self):
		'''
		Returns the unitary normal that defines the plane
		of the Rectangle.
		'''
		# Compute the normal with one side
		v1 = self.points[1] - self.points[0] # P2 - P1
		v2 = self.points[3] - self.points[0] # P4 - P1
		w1 = v2.cross(v1)                    # v2 x v1
		# Compute the normal with the other side
		v3 = self.points[3] - self.points[2] # P4 - P3
		v4 = self.points[1] - self.points[2] # P2 - P3
		w2 = v4.cross(v3)                    # v1 x v2
		# Crash if the normals are not equal!
		if not w1 == w2: raise ValueError('Rectangle must define one plane!')
		return w1/w1.norm()

	def project(self,point):
		'''
		Given a point outside the plane defined by the Rectangle, 
		it projects the point into the Rectangle plane.
		'''
		n = self.normal() # Normal to the plane
		if isinstance(point,Point): 
			# We are dealing with a single point
			vp   = point - self.points[0]
			dist = vp.dot(n)
		else:
			# We are dealing with a list of points
			npoints = point.shape[0]
			n       = np.tile(n._xyz,(npoints,)).reshape(npoints,3)
			vp      = point - np.tile(self.points[0].xyz,(npoints,)).reshape(npoints,3)
			dist    = np.tile(np.sum(vp*n,axis=1),(3,1)).T
		# Projected point in the Rectangle plane
		return point + dist*n

	def inclusion3D(self,point):
		'''
		3D inclusion is easily determined by projecting the point and polygon into 2D. 
		To do this, one simply ignores one of the 3D coordinates and uses the other two.
		To optimally select the coordinate to ignore, compute a normal vector to the plane, 
		and select the coordinate with the largest absolute value [Snyder & Barr, 1987]. 
		This gives the projection of the polygon with maximum area, and results in robust computations.

		This function is for internal use inside the Cube method.
		'''
		n = self.normal()       # Normal to the plane
		p = self.project(point) # Projected point
		# Which is the biggest dimension?
		idmax = np.argmax(np.abs(n.xyz))
		# Convert to xy the smallest dimensions for Rectangle
		for ip in range(self.npoints):
			self.points[ip]._xyz = np.append(np.delete(self.points[ip]._xyz,idmax),np.zeros((1,)))
		# Redo the bounding box
		self._bbox = Ball.fastBall(self)
		# Do the same for the points
		if isinstance(point,Point):
			p._xyz =  np.append(np.delete(p._xyz,idmax),np.zeros((1,)))
		else:
			npoints = p.shape[0]
			p =  np.append(np.delete(p,idmax,axis=1),np.zeros((npoints,1)),axis=1)
		return p

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a square from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 4: raise ValueError('Invalid number of points for Rectangle %d' % npoints)
		return super(Rectangle, cls).from_array(xyz)


class SimpleCube(Polygon):
	'''
	3D cube. Assumes the points to be aligned with the axis.
	For any other shape please use Cube or Polygon.

	  8-------7
	 /|      /|
	4-------3 |
	| 5-----|-6
	|/	    |/
	1-------2
	'''
	def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax):
		pointList = [
			Point(xmin,ymin,zmin), # 1
			Point(xmax,ymin,zmin), # 2
			Point(xmax,ymax,zmin), # 3
			Point(xmin,ymax,zmin), # 4
			Point(xmin,ymin,zmax), # 5
			Point(xmax,ymin,zmax), # 6
			Point(xmax,ymax,zmax), # 7
			Point(xmin,ymax,zmax), # 8
		]
		super(SimpleCube, self).__init__(pointList)

	def isinside(self,point,algorithm=None):
		'''
		A fast algorithm for cubes.
		'''
		x_inside = point[0] >= self.points[0][0] and point[0] <= self.points[1][0]
		y_inside = point[1] >= self.points[0][1] and point[1] <= self.points[3][1]
		z_inside = point[2] >= self.points[0][2] and point[2] <= self.points[7][2]
		return x_inside and y_inside and z_inside

	def areinside(self,xyz,algorithm=None):
		'''
		A fast algorithm for cubes.
		'''
		x_inside = np.logical_and(xyz[:,0] >= self.points[0][0], xyz[:,0] <= self.points[1][0])
		y_inside = np.logical_and(xyz[:,1] >= self.points[0][1], xyz[:,1] <= self.points[3][1])
		z_inside = np.logical_and(xyz[:,2] >= self.points[0][2], xyz[:,2] <= self.points[7][2])
		return np.logical_and(np.logical_and(x_inside,y_inside),z_inside)

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a cube from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 8: raise ValueError('Invalid number of points for Cube %d' % npoints)
		return super(SimpleCube, cls).from_array(xyz)


class Cube(Polygon):
	'''
	3D cube.

	  8-------7
	 /|      /|
	4-------3 |
	| 5-----|-6
	|/	    |/
	1-------2
	'''
	def __init__(self,points):
		if not len(points) == 8: raise ValueError('Invalid Cube!')
		super(Cube, self).__init__(points)

	def isinside(self,point,algorithm=None):
		'''
		Project the point to each of the faces of the cube and check
		if the point is inside or outside of the 2D geometry.
		Each face is a rectangle
		'''
		# Generate the indices for each face
		face_ids = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,6,7,3),(0,3,7,4),(1,2,6,5)]
		# Loop the faces
		for face_id in face_ids:
			print(face_id)
			# Obtain each face as a Rectangle
			face = Rectangle([self.points[face_id[0]],
							  self.points[face_id[1]],
							  self.points[face_id[2]],
							  self.points[face_id[3]]]
							)
			print(face)
			p = face.inclusion3D(point)
			print(face)
			print(point,p)
			# Check if the projected point is inside the face
			inside = face.isinside(p)
			# If the point is outside the face we can already stop
			print(inside)
			if not inside: return False
		# If we reached here it means the point is inside all the faces
		return True

	def areinside(self,xyz,algorithm=None):
		'''
		Project the point to each of the faces of the cube and check
		if the point is inside or outside of the 2D geometry.
		Each face is a rectangle
		'''
		npoints = xyz.shape[0]
		out     = np.ones((npoints,),dtype=bool)
		# Generate the indices for each face
		face_ids = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,6,7,3),(0,3,7,4),(1,2,6,5)]
		# Loop the faces
		for face_id in face_ids:
			# Obtain each face as a Rectangle
			face = Rectangle([self.points[face_id[0]],
							  self.points[face_id[1]],
							  self.points[face_id[2]],
							  self.points[face_id[3]]]
							)
			# Check if the projected points are inside the face
			inside = face.areinside(face.inclusion3D(xyz))
			# Filter out the points that are outside (False)
			out = np.logical_and(out,inside)
		return out

	@classmethod
	def from_array(cls,xyz):
		'''
		Build a cube from an array of points
		of shape (npoints,3).
		'''
		npoints   = xyz.shape[0]
		if not npoints == 8: raise ValueError('Invalid number of points for Cube %d' % npoints)
		return super(Cube, cls).from_array(xyz)