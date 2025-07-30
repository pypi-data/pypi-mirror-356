
from . import point
from . import points
from . import draw
from . import graph
from . import sets

import cairo
from gi.repository import Gdk

def open(p):
	global button
	button=sets.colorButton(set(p),conv_conc,"Arc Orientation")
	return button

def conv_conc(b,d):
	p=point.lastselect
	pnts=points.points
	ix=pnts.index(p)
	if pnts[ix]._inter_ or (ix<(len(pnts)-1) and pnts[ix+1]._inter_):
		if p.get_parent() or pnts[ix+1].get_parent():
			arc_change(p,pnts[ix+1])
			b._set_text_(set(p))
			return
	p._concav_=False if p._concav_ else True
	b._set_text_(set(p))

def set(p):
	if p._concav_:
		return chr(0x23dc)
	else:
		return chr(0x23dd)

def arc_change(p0,p1):
	w=draw.wstore
	h=draw.hstore
	cr=cairo.Context(graph.surface)
	ope=cr.get_operator()
	cr.set_operator(cairo.Operator.CLEAR)
	graph.clearline(cr,p0,p1,w,h)
	cr.set_operator(ope)
	#
	p0._concav_=False if p0._concav_ else True
	#
	co=Gdk.RGBA()
	if co.parse(sets.get_fgcolor2()):
		cr.set_source_rgb(co.red,co.green,co.blue)
	graph.line_draw(cr,p0,p1,w,h)
	graph.area.queue_draw()

