
from gi.repository import Gtk

from . import info
from . import sets

def open(e):
	box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	box.append(sets.colorLabel("The following exception have been occurred:"))
	box.append(sets.colorLabel(e))
	box.append(sets.colorButton("OK",done,"Acknowledgement"))
	info.win.set_child(box)

def done(b,d):
	info.win.set_child(info.box)
