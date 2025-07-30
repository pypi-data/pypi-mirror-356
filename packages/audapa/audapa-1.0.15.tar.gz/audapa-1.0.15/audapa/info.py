
from gi.repository import Gtk

from . import play
from . import sets

#win,box

def open(b,d):
	bx=Gtk.Grid(hexpand=True)
	nchannels, sampwidth, framerate, nframes, comptype, compname = play.wavefile.getparams()
	add(bx,"Name","Value",0,'b')
	add(bx,"nchannels",nchannels.__str__(),1)
	add(bx,"sampwidth",sampwidth.__str__(),2)
	add(bx,"framerate",framerate.__str__(),3)
	add(bx,"nframes",nframes.__str__(),4)
	add(bx,"comptype",comptype,5)
	add(bx,"compname",compname,6)
	bx.attach(sets.colorButton("Done",done,"Back"),0,7,2,1)
	win.set_child(bx)

def add(b,n,v,r,e=None):
	a=sets.colorLabel(n,e)
	a.set_halign(Gtk.Align.START)
	f = Gtk.Frame()
	f.set_hexpand(True)
	f.set_child(a)
	b.attach(f,0,r,1,1)
	a=sets.colorLabel(v,e)
	a.set_halign(Gtk.Align.START)
	f = Gtk.Frame()
	f.set_hexpand(True)
	f.set_child(a)
	b.attach(f,1,r,1,1)

def done(b,d):
	win.set_child(box)
