
from gi.repository import Gtk

from . import sets
from . import bar
from . import draw
from . import r_offset
from . import drawscroll
from . import delete
from . import play
from . import forms
from . import reload
from . import info
from . import goto

on='+'
#off='-'
control=None
char_delete=chr(0x2421)

def init():
	global start,end
	b=Gtk.Box(homogeneous=True)
	start=r_offset.inttext("0")
	start.set_halign(Gtk.Align.START)
	b.append(start)
	end=r_offset.inttext("0")
	end.set_halign(Gtk.Align.END)
	b.append(end)
	return b

def press(g,n,x,y,d):
	r_offset.calculate(int(x if drawscroll.landscape else y))

def add(a,b,i,c,lst):
	d=sets.colorButton(a,b,i,c)
	bar.box.append(d)
	lst.append(d)
	return d
def open():
	global stop,moveleft,moveright
	lst=[]
	button=add(on,toggle,"Selection Mode",draw.cont,lst)
	add(char_delete,delete.act,"Delete",None,lst)
	add(chr(0x1f58b),play.save,"Save All",None,lst)
	add(chr(0x1f58a),play.saveshort,"Save Points",None,lst)
	moveleft=add("&lt;",drawscroll.move,"Left Move (,)",False,lst)
	moveright=add("&gt;",drawscroll.move,"Right Move (.)",True,lst)
	add(chr(0x21B7),goto.open,"Go To",None,lst)
	add(chr(0x24D8),info.open,"Wave information",None,lst)
	stop=add("x",close,"Close",{'b':button,'list':lst},lst)
	#
	drawscroll.open()
	forms.open()
def close(s,d):
	b=d['b']
	if control:
		b.emit(sets._click_)
	for x in d['list']:
		bar.box.remove(x)
	reset()
	draw.close()
	drawscroll.close()
	forms.close()
	reload.close()
def reset():
	start._set_text_("0")
	end._set_text_("0")

def toggle(b,a):
	global control
	if control:
		a.remove_controller(control)
		control=None
		b._set_text_(on)
	else:
		control = Gtk.GestureClick()
		control.connect("pressed",press,None)
		a.add_controller(control)
		b._set_text_('-')
