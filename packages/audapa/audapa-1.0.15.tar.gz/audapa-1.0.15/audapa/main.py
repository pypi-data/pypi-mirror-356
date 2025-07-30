import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from . import loop
from . import sets
from . import play
from . import drawscroll
from . import r_offset
from . import bar
from . import forms
from . import info

def main():
	if len(sys.argv)>1:
		cleanup()
		return
	sets.init()
	win = Gtk.Window()
	win.set_decorated(False)#such a heavy load here if True
	win.maximize()
	win.show()
	#while loop.n:
	play.init()
	drawscroll.init()
	box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	combo=[win,box]
	box.append(bar.init(combo))
	box.append(drawscroll.win)
	box.append(forms.init(combo))
	box.append(r_offset.init())
	win.set_child(box)
	info.win=win
	info.box=box
	loop.main.run()

import os
import sys

def cleanup_dir(d):
	if os.path.isdir(d):
		return d
	return None
def cleanup_dir_rm(d):
	if len(os.listdir(path=d))==0:
		os.rmdir(d)   #OSError if not empty, the check was already
		print(d.__str__()+" removed")
	else:
		print(d.__str__()+" is not empty.")
def cleanup():
	#remove config and exit
	c=cleanup_dir(sets.get_config_dir())
	if c:
		f=sets.get_config_file()
		if not os.path.isfile(f):
			f=None
	p=cleanup_dir(sets.get_data_dir())
	if c or p:
		print("Would remove:");
		if c:
			if f:
				print(f)
			print(c)
		if p:
			print(p)
		print("yes ?");
		str = ""
		while True:
			x = sys.stdin.read(1) # reads one byte at a time, similar to getchar()
			if x == '\n':
				break
			str += x
		if str=="yes":
			if c:
				if f:
					os.remove(f)
					print(f+" removed")
				cleanup_dir_rm(c)
			if p:
				cleanup_dir_rm(p)
		else:
			print("expecting \"yes\"")

if __name__ == "__main__":
    main()
