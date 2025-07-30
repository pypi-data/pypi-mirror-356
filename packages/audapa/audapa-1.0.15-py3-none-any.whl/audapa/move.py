
from gi.repository import Gtk

from . import sets
from . import points
from . import draw
from . import graph
from . import point
from . import level
from . import save

buffer=Gtk.EntryBuffer()
to_right=Gtk.CheckButton()

def open(b,combo):
	bx=Gtk.Grid(hexpand=True)
	bx.attach(sets.colorLabel("Move points N samples"),0,0,1,1)
	bx.attach(sets.colorEntry(buffer),1,0,1,1)
	bx.attach(sets.colorLabel("Right direction"),0,1,1,1) #Left
	bx.attach(to_right,1,1,1,1)
	bx.attach(sets.colorButton("Cancel",cancel,"Abort",combo),0,2,2,1)
	bx.attach(sets.colorButton("Done",done,"Apply",combo),0,3,2,1)
	combo[0].set_child(bx)

def cancel(b,combo):
	combo[0].set_child(combo[1])

def saved(combo):
	combo[0].set_child(combo[1]) #here or problem at surface
	graph.redraw()
	if point.lastselect:
		point.lastselect._info_()

def done(b,combo):
	a=buffer.get_text()
	if a.isdigit():
		s=len(points.points)
		if s>=1:
			b=int(a)
			if to_right.get_active():
				dif=draw.length-points.points[s-1]._offset_
				if b>dif:
					buffer.set_text(dif.__str__(),-1)
					return
				b=-b
			else:
				start=points.points[0]._offset_
				if start<b:
					buffer.set_text(start.__str__(),-1)
					return
			for i in range(0,s):
				points.points[i]._offset_-=b
			saved(combo)
			if sets.get_fulleffect():
				save.effect()
			return
		combo[0].set_child(combo[1])
		return
	level.not_a_digit(buffer)
