
from . import point
from . import draw
from . import graph
from . import drawscroll
from . import points
from . import level

def autodrag(p,x,y):
	p._dend_(x,y)
	graph.area.queue_draw()

def coord(p,h):
	hg=p._height_
	p._height_=h
	x,y=p._coord_(draw.wstore,draw.hstore)
	p._height_=hg
	return x,y

def base(b,d):
	p=point.lastselect
	x,y=coord(p,0)
	autodrag(p,x,y)

#tests: 3 tests on special way

def left(b,d):
	p=point.lastselect
	if p.get_parent(): #only if in current cont, else will be an error, visible and gtk error
		_,y=draw.cont.get_child_position(p)
		y+=point.const
		if drawscroll.landscape:
			ix=points.points.index(p)
			if ix==0 or points.points[ix-1]._offset_<draw.offset:
				autodrag(p,0,y)
			else:
				autodrag(p,points.points[ix-1]._offset_,y)
		else:
			autodrag(p,0,y)

def right(b,d):
	p=point.lastselect
	if p.get_parent():
		_,y=draw.cont.get_child_position(p)
		y+=point.const
		if drawscroll.landscape:
			ix=points.points.index(p)
			sz=len(points.points)
			if ix+1==sz or points.points[ix+1]._offset_>(draw.offset+draw.size):
				autodrag(p,draw.size,y)
			else:
				autodrag(p,points.points[ix+1]._offset_,y)
		else:
			x,_=coord(p,level.get_size()-1)
			autodrag(p,x,y)

def up(b,d):
	p=point.lastselect
	if p.get_parent():
		x,_=draw.cont.get_child_position(p)
		x+=point.const
		if drawscroll.landscape:
			autodrag(p,x,0)
		else:
			ix=points.points.index(p)
			if ix==0 or points.points[ix-1]._offset_<draw.offset:
				autodrag(p,x,0)
			else:
				autodrag(p,x,points.points[ix-1]._offset_)

def down(b,d):
	p=point.lastselect
	if p.get_parent():
		x,_=draw.cont.get_child_position(p)
		x+=point.const
		if drawscroll.landscape:
			_,y=coord(p,level.get_size()-1) #simple get height will fall to 256 ([0,255] are the allowed heights)
			autodrag(p,x,y)
		else:
			ix=points.points.index(p)
			sz=len(points.points)
			if ix+1==sz or points.points[ix+1]._offset_>(draw.offset+draw.size):
				autodrag(p,x,draw.size)
			else:
				autodrag(p,x,points.points[ix+1]._offset_)
