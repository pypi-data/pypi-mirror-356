
import math

from . import points
from . import arc
from . import draw
from . import reload

def data(b,d):
	effect()
def effect():
	apply()
	saved()
def saved():
	reload.file() #for playback , there is a wavefile.readframes at the callback
	redraw()

def redraw():
	draw.surf()
	draw.reset()
	draw.area.queue_draw()

def set(i,v):
	try: #here and 2 more places (about samples length vs points length)
		draw.samples[i]=int(v) #there are troubles at write file without int
	except:
		pass #this can be ignored
def apply():
	s=len(points.points)
	if s>=2:
		for i in range(1,s):
			prev=points.points[i-1]
			cur=points.points[i]
			x0=prev._offset_
			y0=prev._height_
			x1=cur._offset_
			y1=cur._height_
			#print(str(i-1)+"="+str(x0)+","+str(i)+"="+str(x1))
			if cur._inter_ or prev._inter_:
				apply_arc(x0,y0,x1,y1,prev._concav_)
			else:
				apply_line(x0,y0,x1,y1)

def apply_arc(x0,y0,x1,y1,conc):
	x=x1-x0
	y=abs(y1-y0)
	#get radius
	radius,rads=arc.radius(x,y)
	#get center
	_,yc,rstart,rend=arc.center(x0,y0,x1,y1,conc,x,y,radius,rads)
	#iterate
	if rstart==0 or rend==math.pi or rstart==math.pi or rend==0:
	#x axis
		xpos=radius-x
		if rstart==0 or rend==0:
			startpoint=0
			stoppoint=x
			#print(4 if rend==0 else 1)
		else:
			startpoint=1
			stoppoint=x+1
			#print(2 if rstart==math.pi else 3)
		for i in range(startpoint,stoppoint):
			#supra radius
			a=xpos/radius
			#to radians
			a=math.acos(a)
			#height
			h=math.sin(a)*radius
			if rstart==0:
				set(x0+i,y1+h)
			elif rstart==math.pi:
				set(x1-i,y0-h)
			elif rend==math.pi:
				set(x1-i,y0+h)
			else:
			#rend==0
				set(x0+i,y1-h)
			xpos+=1
	else:
	#y axis
		if rstart==math.pi*3/2 or rend==math.pi/2:
			startpoint=x-1
			stoppoint=-1
			#print(6 if rstart==math.pi*3/2 else 7)
		else:
			startpoint=x
			stoppoint=0
			#print(5 if rstart==math.pi/2 else 8)
		for i in range(startpoint,stoppoint,-1):
			a=i/radius
			a=math.asin(a)
			h=math.cos(a)*radius
			if rstart==math.pi/2:
				set(x1-i,yc+h)
			elif rstart==math.pi*3/2:
				set(x0+i,yc-h)
			elif rend==math.pi/2:
				set(x0+i,yc+h)
			else:
			#rend==math.pi*3/2
				set(x1-i,yc-h)

def apply_line(x0,y0,x1,y1):
	if x0!=x1: #a will be inf and also no for
		x=x1-x0
		y=y1-y0
		a=y/x
		for i in range(0,x):
			y=a*i
			set(x0+i,y0+y)
