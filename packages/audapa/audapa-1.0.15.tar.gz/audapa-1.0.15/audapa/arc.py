
from . import drawscroll
from . import graph
from . import point

import math

def draw(cr,x0,y0,x1,y1,concav):
	land=drawscroll.landscape
	if land:
		x=x1-x0
		y=abs(y1-y0)
	else:
		x=abs(x1-x0)
		y=y1-y0
	c,raddif=radius(x,y)
	xc,yc,rstart,rend=center(x0,y0,x1,y1,concav,x,y,c,raddif,land)
	#will be a heavy cpu load with radsmall when moveing an inter up a stable at angle 0 cr.arc(xc,yc,c,rstart+radsmall,rend-radsmall)
	cr.arc(xc,yc,c,rstart,rend)
def center(x0,y0,x1,y1,concav,x,y,c,raddif,land=True):
	if land:
		if concav: #concav on land
			if x>y:
				if y0<y1:
					#...
					#   ...
					xc=x0
					yc=y0+c
					#if raddif!=None:
					a=math.pi*3/2
					b=math.pi*3/2+raddif
				else:
					#   ...
					#...
					xc=x1
					yc=y1+c
					a=math.pi*3/2-raddif
					b=math.pi*3/2
			else:
				if y0<y1:
					#.
					#.
					# .
					# .
					xc=x1-c
					yc=y1
					a=-raddif
					b=0
				else:
					# .
					# .
					#.
					#.
					xc=x0+c
					yc=y0
					a=math.pi
					b=math.pi+raddif
		else:
			if x>y:
				if y0<y1:
					#...
					#   ...
					xc=x1
					yc=y1-c
					a=math.pi/2
					b=math.pi/2+raddif
				else:
					#   ...
					#...
					xc=x0
					yc=y0-c
					a=math.pi/2-raddif
					b=math.pi/2
			else:
				if y0<y1:
					#.
					#.
					# .
					# .
					xc=x0+c
					yc=y0
					a=math.pi-raddif
					b=math.pi
				else:
					# .
					# .
					#.
					#.
					xc=x1-c
					yc=y1
					a=0
					b=raddif
	else:
		if concav:
			if x>y:
				if x0<x1:
					#...
					#   ...
					xc=x1
					yc=y1-c
					a=math.pi/2
					b=math.pi/2+raddif
				else:
					#   ...
					#...
					xc=x0
					yc=y0+c
					a=math.pi*3/2-raddif
					b=math.pi*3/2
			else:
				if x0<x1:
					#.
					#.
					# .
					# .
					xc=x0+c
					yc=y0
					a=math.pi-raddif
					b=math.pi
				else:
					# .
					# .
					#.
					#.
					xc=x1+c
					yc=y1
					a=math.pi
					b=math.pi+raddif
		else:
			if x>y:
				if x0<x1:
					#...
					#   ...
					xc=x0
					yc=y0+c
					a=math.pi*3/2
					b=math.pi*3/2+raddif
				else:
					#   ...
					#...
					xc=x1
					yc=y1-c
					a=math.pi/2-raddif
					b=math.pi/2
			else:
				if x0<x1:
					#.
					#.
					# .
					# .
					xc=x1-c
					yc=y1
					a=-raddif
					b=0
				else:
					# .
					# .
					#.
					#.
					xc=x0-c
					yc=y0
					a=0
					b=raddif
	return (xc,yc,a,b)
def radius(x,y):
	if x>y:
		n=x
		m=y
	else:
		n=y
		m=x
	rbig=graph.rads(n,m)
	rsmall=math.pi/2-rbig
	dif=rbig-rsmall
	cat2=n/math.cos(dif)
	return (cat2,math.pi/2-dif)
#def vals(x,y):
#	c,raddif,rads=radius(x,y)
#	l=point.const
#	aux=math.cos(rads)
#	ad=aux*l
#	op=math.sin(rads)*l
#	radsmall=math.atan2(op,c-ad)
#	return (c,raddif,radsmall)
