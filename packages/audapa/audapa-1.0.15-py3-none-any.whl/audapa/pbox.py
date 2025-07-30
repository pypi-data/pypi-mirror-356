
from gi.repository import Gtk

from . import sets
from . import seloff
from . import forms
from . import point
from . import points
from . import draw
from . import graph
from . import arcbutton
from . import step
from . import snap

def open(p):
	global box,info
	box=Gtk.Box()
	sep=Gtk.Separator() #margin-start=0
	sep.set_margin_start(4)
	sep.set_margin_end(4)
	box.append(sep)
	box.append(arcbutton.open(p))
	#box.append(sets.colorButton(chr(0x0077),manual,"Manual"))#0057
	#def manual(b,d):
	box.append(sets.colorButton(seloff.char_delete,delete,"Delete"))
	a=chr(0x2B05)
	box.append(sets.colorButton(a,step.left,"Left ("+a+")"))
	a=chr(0x27A1)
	box.append(sets.colorButton(a,step.right,"Right ("+a+")"))
	a=chr(0x2B06)
	box.append(sets.colorButton(a,step.up,"Up ("+a+")"))
	a=chr(0x2B07)
	box.append(sets.colorButton(a,step.down,"Down ("+a+")"))
	box.append(sets.colorButton(chr(0x2693),snap.base,"Snap to base"))
	box.append(sets.colorButton(chr(0x21E4),snap.left,"Snap Left"))
	box.append(sets.colorButton(chr(0x21E5),snap.right,"Snap Right"))
	box.append(sets.colorButton(chr(0x2912),snap.up,"Snap Up"))
	box.append(sets.colorButton(chr(0x2913),snap.down,"Snap Down"))
	info=sets.colorLabel(inf(p))
	info.set_hexpand(True) #Default value: FALSE
	info.set_halign(Gtk.Align.END)
	box.append(info)
	forms.box.set_halign(Gtk.Align.START)
	forms.box.set_hexpand(False)
	forms.box.get_parent().append(box)

def close():
	forms.box.get_parent().remove(box)
	forms.box.set_hexpand(True)
	forms.box.set_halign(Gtk.Align.CENTER)

def delete(b,d):
	p=point.lastselect
	ix=points.points.index(p)
	dels,puts=p._take_(ix)
	ix=and_inter(ix,dels,puts)
	graph.lines(dels,puts,draw.wstore,draw.hstore)
	p._remove_(ix)
	if p.get_parent():
		p.get_parent().remove(p)
	close()
	point.lastselect=None
	graph.area.queue_draw()
def and_inter(ix,dels,puts):
	pnts=points.points
	sz=len(pnts)
	if ix==0:
		if sz==1:
			return ix
		if and_inter_test(1):
			dels.append([dels[0][1],pnts[1]])
	elif ix==(sz-1):
		if and_inter_test(sz-2):
			dels.append([pnts[sz-3],dels[0][0]])
			ix-=1
	elif pnts[ix-1]._inter_:
		if and_inter_test(ix+1):
			aux=pnts[ix+1]
			dels.append([dels[1][1],aux])
			puts[0][1]=aux
	return ix
def and_inter_test(test):
	p=points.points[test]
	b=p._inter_
	if b:
		p._remove_(test)
		if p.get_parent():
			p.get_parent().remove(p)
	return b

def inf(p):
	return str(p._offset_)+' '+str(p._height_)
