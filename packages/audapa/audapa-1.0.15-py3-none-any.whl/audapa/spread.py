
from gi.repository import Gtk

from . import sets
from . import points
from . import level
from . import draw
from . import blank
from . import move
from . import save
from . import distance

spread=Gtk.EntryBuffer()
reduce=Gtk.CheckButton()

#box,pointsorig,samplesorig,distancebutton

def open(b,combo):
	global box
	box=Gtk.Grid(hexpand=True)
	box.attach(sets.colorLabel("Spread/Compress N samples"),0,0,1,1)
	box.attach(sets.colorEntry(spread),1,0,1,1)
	box.attach(sets.colorLabel("Compress"),0,1,1,1) #Enlarge
	box.attach(reduce,1,1,1,1)
	box.attach(sets.colorButton("Cancel",cancel,"Abort",combo),0,2,2,1)
	box.attach(sets.colorButton("Done",done,"Apply",combo),0,3,2,1)
	try:
		global pointsorig,samplesorig
		#if from previous compress
		del pointsorig
		del samplesorig
	except:
		pass
	global distancebutton
	distancebutton=None
	combo[0].set_child(box)

def cancel(b,combo):
	try:
		restore()
		draw.samples=samplesorig
	except:
		pass
	combo[0].set_child(combo[1])
def restore():
	for i in range(0,len(pointsorig)): #pointsorig can be modified it will not influence the starting for-to
		points.points[i]._offset_=pointsorig[i]

def done(b,combo):
	a=spread.get_text()
	if a.isdigit():
		ps=points.points
		s=len(ps)
		if s>=2:
			b=int(a)
			if reduce.get_active():
				try:
					#can be in vain , is return after, but who cares about that return
					restore()
				except:
					global pointsorig
					pointsorig=[]
					for p in points.points:
						pointsorig.append(p._offset_)
				end=ps[s-1]._offset_
				n=end-ps[0]._offset_
				if b>n:
					spread.set_text(n.__str__(),-1)
					return
				apply(-b,-1)
				if sets.get_fulleffect():
					global samplesorig
					try:
						draw.samples=samplesorig.copy() #can hit done multiple times and then is .copy
					except:
						samplesorig=draw.samples.copy()
					compress(b,end)
				if dtest:=distance.test_all():
					global distancebutton
					a=distancebutton
					distancebutton=distance.hold(dtest,distancebutton,callback,combo)
					if not a:
						box.attach(distancebutton,0,4,2,1)
					return
			else:
				if sets.get_fulleffect():
					enlarge(b)
				apply(b,1)
			conclude(combo)
			return
		combo[0].set_child(combo[1])
		return
	level.not_a_digit(spread)
def conclude(combo):
	move.saved(combo)
	if sets.get_fulleffect():
		blank.saved()
		save.effect()
def callback(b,combo):
	conclude(combo)

def enlarge(n):
	s=len(draw.samples)
	extra=s-points.points[len(points.points)-1]._offset_
	#there is a nicer move but this is lazy
	right=draw.samples[s-extra:]
	del draw.samples[s-extra:]
	draw.samples=draw.samples+([0]*n)+right

def compress(n,end):
	#copy right at position
	s=len(draw.samples)
	extra=s-end
	for i in range(end,s):
		draw.samples[i-n]=draw.samples[i]
	#remove N in safe
	del draw.samples[s-n:]

def apply(n,sign):
	ps=points.points
	leng=len(ps)
	total=ps[leng-1]._offset_-ps[0]._offset_
	rest=[]
	rest_sum=0
	for i in range(1,leng):
		sz=(ps[i]._offset_-ps[i-1]._offset_)*n
		sp=int(sz/total)
		rs=sz%total
		ps[i]._offset_+=sp
		rest.append([rs,i])
		rest_sum+=rs
		for j in range(i+1,leng):
			ps[j]._offset_+=sp
	rest.sort(reverse=True) #by first
	unassigned=int(rest_sum/total) #'float' object cannot be interpreted as an integer
	for i in range(0,unassigned):
		pos=rest[i][1]
		ps[pos]._offset_+=sign
		for j in range(pos+1,leng):
			ps[j]._offset_+=sign
