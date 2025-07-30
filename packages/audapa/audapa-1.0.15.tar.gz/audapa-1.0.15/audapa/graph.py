
from gi.repository import Gtk,Gdk
import cairo
import math

from . import points
from . import sets
from . import drawscroll
from . import arc
from . import draw
from . import forms

def open(ovr):
	global area
	area=Gtk.DrawingArea()
	area.set_draw_func(draw_cont,None,None)
	ovr.add_overlay(area)
def close(ovr):
	ovr.remove_overlay(area)
def draw_cont(widget,cr,width,height,d,d2):
	cr.set_source_surface(surface, 0, 0)
	cr.paint()
def surf(w,h):
	global surface
	surface = area.get_native().get_surface().create_similar_surface(cairo.Content.COLOR_ALPHA,w,h)

def put(ix,c1,w,h):
	if ix>0:
		c0=points.points[ix-1]
		line(c0,c1,w,h)
	elif len(points.points)>1:
		c0=points.points[1]
		line(c1,c0,w,h)
def line(c0,c1,w,h):
	cr=cairo.Context(surface)
	co=Gdk.RGBA()
	if co.parse(sets.get_fgcolor2()):
		cr.set_source_rgb(co.red,co.green,co.blue)
	line_draw(cr,c0,c1,w,h)
def line_draw(cr,c0,c1,w,h):
	a0=c0._coord_(w,h)
	a1=c1._coord_(w,h)
	if c0._inter_ or c1._inter_:
		arc.draw(cr,a0[0],a0[1],a1[0],a1[1],c0._concav_)
	else:
		#don't let line width corners to intersect
		p0,p1=coords(a0[0],a0[1],a1[0],a1[1])
		cr.move_to(p0[0],p0[1])
		cr.line_to(p1[0],p1[1])
	cr.stroke()
def lines(dels,puts,w,h):
	cr=cairo.Context(surface)
	ope=cr.get_operator()
	cr.set_operator(cairo.Operator.CLEAR)
	for d in dels:
		clearline(cr,d[0],d[1],w,h)
	cr.set_operator(ope)
	co=Gdk.RGBA()
	if co.parse(sets.get_fgcolor2()):
		cr.set_source_rgb(co.red,co.green,co.blue)
	for p in puts:
		line_draw(cr,p[0],p[1],w,h)
def dels(ds,w,h):
	cr=cairo.Context(surface)
	cr.set_operator(cairo.Operator.CLEAR)
	for d in ds:
		clearline(cr,d[0],d[1],w,h)
def take(ix,pnt):
	sz=len(points.points)
	if ix>0:
		d=[[points.points[ix-1],pnt]]
		if ix+1<sz:
			d.append([pnt,points.points[ix+1]])
		return d
	elif sz>1:
		c0=points.points[1]
		return [[pnt,c0]]
	return None
def clearline(cr,a0,a1,w,h):
	c0=a0._coord_(w,h)
	c1=a1._coord_(w,h)
	#arc is lineing to circle start, not convenient
	if a0._inter_ or a1._inter_:
		arc.draw(cr,c0[0],c0[1],c1[0],c1[1],a0._concav_)
		lw=cr.get_line_width()
		cr.set_line_width(lw+1)  #only this here
		cr.stroke()
		cr.set_line_width(lw)
		return
	x,y=coords0(c0[0],c0[1],c1[0],c1[1],1)   #it's tested
	p0=[c0[0]+x,c0[1]+y]
	p1=[c1[0]-x,c1[1]-y]
	h=cr.get_line_width()/2+1   #it's tested
	x,y=xy_h(h,x,y)
	cr.move_to(p0[0]-x,p0[1]+y)
	cr.line_to(p0[0]+x,p0[1]-y)
	#
	cr.line_to(p1[0]+x,p1[1]-y)
	cr.line_to(p1[0]-x,p1[1]+y)
	#
	cr.line_to(p0[0]-x,p0[1]+y)
	cr.fill()

def coords0(x0,y0,x1,y1,extra=0):
	x=x1-x0
	y=y1-y0
	#l=point.const-extra there was a problem at arc at same thing with this
	l=-extra
	if drawscroll.landscape:
		r=rads(y,x)
		x=math.cos(r)*l
		y=math.sin(r)*l
	else:
		r=rads(x,y)
		x=math.sin(r)*l
		y=math.cos(r)*l
	return (x,y)
def coords(x0,y0,x1,y1):
	x,y=coords0(x0,y0,x1,y1)
	return ([x0+x,y0+y],[x1-x,y1-y])
def xy_h(h,x,y):
	if drawscroll.landscape:
		r=math.atan2(y,x)
		return (math.sin(r)*h,math.cos(r)*h)
	r=math.atan2(x,y)
	return (math.cos(r)*h,math.sin(r)*h)
def rads(a,b):
#this is atan2
	t=a/b if b else math.inf
	return math.atan(t)

def redraw():
	surf(draw.wstore,draw.hstore)
	forms.redraw(draw.wstore,draw.hstore)
	area.queue_draw()
