
from . import seloff
from . import draw
from . import r_offset
from . import drawscroll
from . import reload

def act(b,d):
	st=seloff.start._get_()
	en=seloff.end._get_()
	del draw.samples[st:en]
	draw.length-=en-st
	rem=r_offset.atleft._get_()
	if(rem>=draw.length):
		#offset will be somewhere less than it is now
		n=drawscroll.win.get_width() if drawscroll.landscape else drawscroll.win.get_height()
		draw.offset=max(0,st-int(n/2))
	else:
		#reset
		draw.reset()
	draw.redraw()
	seloff.reset()
	changed()
	#for playback
	reload.file()

def changed():
	r_offset.cged(drawscroll.win.get_hadjustment()) if drawscroll.landscape else r_offset.cged(drawscroll.win.get_vadjustment())
