
from gi.repository import Gtk

from . import info
from . import sets
from . import drawscroll
from . import draw
from . import level
from . import r_offset

def open(b,d):
	box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	bx=Gtk.Box()
	cur,max=get_vals()
	bx.append(sets.colorLabel(cur.__str__()+" 0-"))
	x=max.__str__()
	maxlab=sets.colorLabel(x)
	bx.append(maxlab)
	buf=Gtk.EntryBuffer()
	bx.append(sets.colorEntry(buf))
	bx.append(sets.colorButton("Go",go,"Proceed",[max,buf]))
	box.append(bx)
	box.append(sets.colorButton("First",callback,"Start",0))
	a=0 if cur==0 else (cur-1)
	box.append(sets.colorButton("Previous",callback,a.__str__(),a))
	a=x if cur==max else (cur+1)
	box.append(sets.colorButton("Next",callback,a.__str__(),a))
	box.append(sets.colorButton("Last",callback,"End",max))
	box.append(sets.colorButton("Cancel",cancel,"Abort"))
	info.win.set_child(box)

def cancel(b,combo):
	finish()
def finish():
	info.win.set_child(info.box)
def done(a):
	draw.offset=page()*a
	finish()
	r_offset.cged(adjust())
	draw.redraw()

def callback(b,a):
	done(a)

def page():
	if drawscroll.landscape:
		return drawscroll.win.get_width()*drawscroll.factor
	return drawscroll.win.get_width()*drawscroll.factor
def adjust():
	if drawscroll.landscape:
		return drawscroll.win.get_hadjustment()
	return drawscroll.win.get_vadjustment()

def get_vals():
	of=draw.offset
	p=page()
	cur=int(of/p)
	max=int(draw.length/p)
	return (cur,max)

def go(b,d):
	max,buf=d
	a=buf.get_text()
	if a.isdigit():
		b=int(a)
		if b>max:
			buf.set_text(max.__str__(),-1)
			return
		done(b)
		return
	level.not_a_digit(buf)
