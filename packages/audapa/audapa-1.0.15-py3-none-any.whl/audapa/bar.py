
from gi.repository import Gtk

from . import loop
from . import record
from . import sets
from . import play
from . import build

def min(b,win):
	win.minimize()
	
def cl(b,d):
	loop.stop()

input=0x1F399

def init(combo):
	global box
	box=Gtk.Box()
	box.append(sets.colorButton(chr(input), record.start, "Record audio", input))
	box.append(sets.colorButton(chr(0x2699), sets.sets, "Settings", combo))
	box.append(sets.colorButton("_", min, "Minimize", combo[0]))
	box.append(sets.colorButton("X", cl, "Exit"))
	box.append(play.entry)
	box.append(play.openbutton)
	box.append(play.button)
	box.append(build.init())
	return box
