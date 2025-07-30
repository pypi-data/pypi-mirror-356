
from gi.repository import GLib

from . import record
from . import play

def stop():
	record.terminate()
	play.terminate()
	main.quit()
	#global n
	#n=x

main = GLib.MainLoop()
#n=True
