
import os

from . import play
from . import points

def file():
	global temp
	temp=loc()
	play.save_opened(temp)
	play.wavefile.close()
	play.wave_open(temp)

def loc():
	return points.fpath(play.entry.get_text(),"temp")

def close():
	#temp=loc()
	try:  #can change the entry and temp need to be the last one, but then can be nothing, then use try
		if os.path.exists(temp):
			os.remove(temp)
	except:
		pass
