/* 
	GEOMETRY
	
	Definition of a generic geometric tools such as polygons.

	Arnau Miro (OGS) (c) 2019
*/

#include "geometry.h"

namespace Geom
{
	/* FASTBALL

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
	*/
	void Ball::fastBall(const Polygon &p) {

		double xmin, xmax, ymin, ymax;      // bounding box extremes
		int   Pxmin, Pxmax, Pymin, Pymax;   // index of  P[] at box extreme

		// Find a large diameter to start with
		// first get the bounding box and P[] extreme points for it
		xmin = xmax = p[0][0];
		ymin = ymax = p[0][1];
		Pxmin = Pxmax = Pymin = Pymax = 0;

		for (int ii=1; ii<p.get_npoints(); ++ii) {
			if (p[ii][0] < xmin) {
				xmin = p[ii][0]; Pxmin = ii;
			} else if (p[ii][0] > xmax) {
				xmax = p[ii][0]; Pxmax = ii;
			}
			if (p[ii][1] < ymin) {
				ymin = p[ii][1]; Pymin = ii;
			} else if (p[ii][1] > ymax) {
				ymax = p[ii][1]; Pymax = ii;
			}
		}

		// Select the largest extent as an initial diameter for the  ball
		Point C;
		Vector dPx = p[Pxmax] - p[Pxmin], dPy = p[Pymax] - p[Pymin];
		double rad2, dx2 = dPx.norm2(), dy2 = dPy.norm2();

		if (dx2 >= dy2) {  // x direction is largest extent
			C = p[Pxmin] + (dPx/2.); rad2 = p[Pxmax].dist2(C);
		} else {
			C = p[Pymin] + (dPy/2.); rad2 = p[Pymax].dist2(C);
		}
		double rad = std::sqrt(rad2);

		// Now check that all points p[i] are in the ball
		// and if not, expand the ball just enough to include them
    	Vector dP; double dist, dist2;

    	for (int ii=0; ii<p.get_npoints(); ++ii) {
    		dP = p[ii] - C; dist2 = dP.norm2();
    		if (dist2 <= rad2) continue; // p[i] is inside the ball already
    		// p[i] not in ball, so expand ball  to include it
    		dist = sqrt(dist2); rad = (rad + dist)/2.; rad2 = rad*rad; // enlarge radius just enough
    		C = C + dP*((dist-rad)/dist);                              // shift Center toward p[i]
    	}

    	// Set ball parameters
    	this->set_center(C);
    	this->set_radius(rad);
	}

	/* CN_PINPOLY

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
	*/
	int cn_PinPoly(const Polygon *poly, const Point &P) {

		int cn = 0; // The crossing number counter

		// Loop through all edges of the Polygon
		for (int ii=0; ii<poly->get_npoints(); ++ii) {
			if ( (((*poly)[ii][1] <= P[1]) && ((*poly)[ii+1][1] >  P[1]))         // an upward crossing
			  || (((*poly)[ii][1] >  P[1]) && ((*poly)[ii+1][1] <= P[1])) ) {     // a downward crossing

			  	// Compute  the actual edge-ray intersect x-coordinate
				double vt = (double)( (P[1]  - (*poly)[ii][1]) / ((*poly)[ii+1][1] - (*poly)[ii][1]) );
				if (P[0] <  (*poly)[ii][0] + vt * ((*poly)[ii+1][0] - (*poly)[ii][0]))  // P.x < intersect
					++cn; // A valid crossing of y=P.y right of P.x		
			}
		}
		return(cn & 1); // 0 if even (out), and 1 if  odd (in)
	}

	/* WN_PINPOLY

		Winding number test for a point in a polygon.

		Input:   P = a point,
		Return:  wn = the winding number (=0 only when P is outside)

		from: http://geomalgorithms.com/a03-_inclusion.html

		Copyright 2001 softSurfer, 2012 Dan Sunday
		This code may be freely used and modified for any purpose
		providing that this copyright notice is included with it.
		SoftSurfer makes no warranty for this code, and cannot be held
		liable for any real or imagined damage resulting from its use.
		Users of this code must verify correctness for their application.
	*/
	int wn_PinPoly(const Polygon *poly, const Point &P) {

		int wn = 0; // The  winding number counter

		// Loop through all edges of the polygon
		for (int ii=0; ii<poly->get_npoints(); ++ii) {   // edge from V[i] to  V[i+1]
			if ((*poly)[ii][1] <= P[1]) {   	// start y <= P.y
				if ((*poly)[ii+1][1] > P[1])			// an upward crossing
					if ( P.isLeft((*poly)[ii],(*poly)[ii+1]) > 0 ) // P left of  edge
						++wn; // have  a valid up intersect
			} else {                        // start y > P.y (no test needed)
				if ((*poly)[ii+1][1] <= P[1])	// a downward crossing
					if ( P.isLeft((*poly)[ii],(*poly)[ii+1]) < 0 ) // P left of  edge
						--wn; // have  a valid down intersect
			}
		}
		return wn;
	}	
}