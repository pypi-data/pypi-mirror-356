
from gi.repository import Gtk

import os
import pathlib
import json
import time

from . import sets   #colorLabel,...
from . import play   #wavefile,entry
from . import draw   #samples,...
from . import points #points,...
from . import save   #apply,...
from . import point  #lastselect
from . import move   #saved
from . import pbox   #close

default_toler="1"
toler=Gtk.EntryBuffer(text=default_toler)

#there is a min dist in Settigs, why another one? That is for manually placed points.
default_mdist="5"
mdist=Gtk.EntryBuffer(text=default_mdist)

stop=Gtk.CheckButton()
default_stop="100"
stop_after=Gtk.EntryBuffer(text=default_stop)

print_test=Gtk.CheckButton()
tests_str1="dif sum "
tests_str2="points len "
tests_str3="phase1/orig "

skip_phase2=Gtk.CheckButton()
pause=Gtk.CheckButton()
default_pause="100"
pause_points=Gtk.EntryBuffer(text=default_pause)
pause_points_minimum=1

#tests_time

def data(b,combo):
	box=Gtk.Grid(hexpand=True)

	box.attach(sets.colorLabel("Tolerance"),0,0,2,1)
	box.attach(sets.colorEntry(toler),2,0,1,1)
	box.attach(sets.colorLabel("‰"),3,0,1,1)

	box.attach(sets.colorLabel("Min distance"),0,1,2,1)
	box.attach(sets.colorEntry(mdist),2,1,2,1)

	box.attach(sets.colorLabel("Stop after N non-inter points"),0,2,1,1)
	box.attach(stop,1,2,1,1)
	box.attach(sets.colorEntry(stop_after),2,2,2,1)

	box.attach(sets.colorLabel("Skip phase 2"),0,3,2,1)
	box.attach(skip_phase2,2,3,2,1)

	common_options(box,4)

	pos=6
	if fastpath(False):
		box.attach(sets.colorButton("Fast Resume",restore,"Restore",combo),0,pos,4,1)
		pos+=1

	box.attach(sets.colorButton("Cancel",cancel,"Abort",combo),0,pos,4,1)
	box.attach(sets.colorButton("Done",done,"Apply",combo),0,pos+1,4,1)
	combo[0].set_child(box)

def common_options(box,column):
	box.attach(sets.colorLabel("Verbosity"),0,column,2,1)
	box.attach(print_test,2,column,2,1)
	column+=1

	box.attach(sets.colorLabel("At phase 2, pause every N points"),0,column,1,1)
	box.attach(pause,1,column,1,1)
	box.attach(sets.colorEntry(pause_points),2,column,2,1)

def cancel(b,combo):
	combo[0].set_child(combo[1])

def done(b,combo):
	a=toler.get_text()
	abool=a.isdigit()
	b=mdist.get_text()
	bbool=b.isdigit()
	c=stop_after.get_text()
	cbool=c.isdigit()
	d=pause_points.get_text()
	dbool=d.isdigit()
	if abool and bbool and cbool and dbool:
		a=int(a)
		b=int(b)
		c=int(c)
		d=int(d)
		if a>1000:
			toler.set_text("1000",-1)
		elif b==0:
			mdist.set_text("1",-1)
		elif c<2:
			stop_after.set_text("2",-1)
		elif d<pause_points_minimum:
			pause_points.set_text(str(pause_points_minimum),-1)
		else:
			a=round(pow(2,8*play.wavefile.getsampwidth())*a/1000)

			points.points.clear()

			pack=worker(a,b,c,d,draw.samples.copy(),combo)
			if pack!=None:
				waiter(combo,pack)
	else:
		if not abool:
			toler.set_text(default_toler,-1)
		if not bbool:
			mdist.set_text(default_mdist,-1)
		if not cbool:
			stop_after.set_text(default_stop,-1)
		if not dbool:
			pause_points.set_text(default_pause,-1)

def precalculate1():
	points.add(0,0,False,True,0) #p1
	points.add(0,0,False,True,1) #p2
def precalculate2():
	points.add(0,0,False,True,2) #p3
	points.points[1]._inter_=True

#None/continue_pack
def calculate(samples,length,tolerance,min_dist,max,pause_after,samplesorig):
	#exclude blank extremes
	for i in range(0,length): #not including length element
		if samples[i]!=0:
			break
	for j in range(length-1,-1,-1):
		if samples[j]!=0:
			break
	j=j+1

	if (i+min_dist+1)<j: #only if there is a length of min 2 points
		pnts=[]
		pnts.append(points.newp(i,samples[i],False,True))

		precalculate1()

		if print_test.get_active():
			tests=0
			tests2=0
			tests3=0

		while (i+min_dist+1)<j:  #j can be length
			points.points[0]._offset_=i
			points.points[0]._height_=samplesorig[i]

			for k in range(i+min_dist+1,j):
				points.points[1]._offset_=k
				points.points[1]._height_=samplesorig[k]
				save.apply() #or save.apply_line, will exclude at right
				newdif=0
				for l in range(i,k):
					newdif+=abs(samples[l]-samplesorig[l])

				if newdif>tolerance: #get back one place
					k=k-1
					samples[k]=samplesorig[k]  #this can be restored at last, why not there? who cares, too much code
					points.points[1]._offset_=k
					points.points[1]._height_=samplesorig[k]
					save.apply()
					if print_test.get_active():
						newdif=0
						for l in range(i,k):
							newdif+=abs(samples[l]-samplesorig[l])
					break
			pnts.append(points.newp(k,samplesorig[k],False,True)) #'struct' object has no attribute 'copy'

			if print_test.get_active():
				tests+=newdif
				tests2+=k-i
				for l in range(i,k):
					tests3+=abs(samplesorig[l])

			if stop.get_active():
				if len(pnts)==max:
					break

			i=k
		if print_test.get_active():
			print(tests_str1+str(tests))  #the two tolerances at start will trade precision for more code
			print(tests_str2+str(len(pnts)))
			print(tests_str3+str(tests/tests3))
			print("avg dist "+str(tests2/len(pnts)))
			testspack=[0,0,0,0,0]
		else:
			testspack=[]

		#phase 2 apply arcs for better match
		pnts2=pnts.copy()
		if skip_phase2.get_active()==False:
			precalculate2()

			i,ix,is_done=calculate_resume(pnts,pnts2,samples,samplesorig,0,0,pause_after,testspack)
			if is_done==False:
				return [pnts,pnts2,samples,samplesorig,i,ix,pause_after,testspack]

		points.points=pnts2
	return None

def tests_phase2(pnts2,testspack,remainings):
	print()
	print(tests_str1+str(testspack[0]))
	print(tests_str2+str(len(pnts2)))
	p1_o=testspack[2]/testspack[1]
	print(tests_str3+str(p1_o))
	d_o=testspack[0]/testspack[1]
	print("dif/orig "+str(d_o))
	print(" change "+str(d_o-p1_o))

	t=time.time()-tests_time
	testspack[3]+=1
	testspack[4]+=t
	print("seconds/pauses "+str(int(testspack[4]/testspack[3]))) #time.time() is float
	if remainings:
		print("remaining points "+str(remainings))

def arc(a,b,xleft,xright,ystart,yend,bestmatch,samples,samplesorig):
	points.points[0]._concav_=a;points.points[1]._concav_=b
	for x in range(xleft,xright):
		points.points[1]._offset_=x
		for y in range(ystart,yend):
			points.points[1]._height_=y
			save.apply() #or save.apply_arc

			thisdif=0
			for k in range(xleft,xright):
				thisdif+=abs(samples[k]-samplesorig[k])

			if thisdif<bestmatch[0]:
				bestmatch[0]=thisdif
				bestmatch[1]=a
				bestmatch[2]=b
				bestmatch[3]=x
				bestmatch[4]=y

def waiter(combo,pack):
	box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	box.append(sets.colorLabel("Resume Screen"))
	box.append(sets.colorButton("Fast Resume Save &amp; Done",fastsavedone,"Restore Save & Stop",[pack,combo]))
	box.append(sets.colorButton("Fast Resume Save &amp; Resume",fastsaveresume,"Restore Save & Resume",[pack,combo]))
	box.append(sets.colorButton("Resume",resumefn,"Continue",[pack,combo]))
	combo[0].set_child(box)

def resumefn(b,bigpack):
	pack,combo=bigpack
	resume(combo,pack)

def terminate(combo,pnts2,samplesorig,testspack):
	points.points=pnts2
	finish(samplesorig,combo)

def resume(combo,pack):
	pnts2=pack[1];samplesorig=pack[3];testspack=pack[7]
	pack[4],pack[5],is_done=calculate_resume(pack[0],pnts2,pack[2],samplesorig,pack[4],pack[5],pack[6],testspack)
	if is_done:
		terminate(combo,pnts2,samplesorig,testspack)
		fastsavefinish()

#same as calculate+for finish
def worker(tolerance,min_dist,max,pause_after,samplesorig,combo): #used to not store height on another var at phase1, and at phase2
	pack=calculate(draw.samples,draw.length,tolerance,min_dist,max,pause_after,samplesorig)
	if pack!=None:
		return pack
	finish(samplesorig,combo)
	fastsavefinish()
	return None

def finish(samplesorig,combo):
	if point.lastselect:
		pbox.close()
		point.lastselect=None
	if not sets.get_fulleffect():
		draw.samples=samplesorig
	move.saved(combo)
	if sets.get_fulleffect():
		save.saved()

#i,ix,is_done
def calculate_resume(pnts,pnts2,samples,samplesorig,i,ix,pause_after,testspack):
	if print_test.get_active():
		global tests_time
		tests_time=time.time()

	aux=points.points[1]
	sz=len(pnts)-1
	for i in range(i,sz):
		xleft=pnts[i]._offset_;xright=pnts[i+1]._offset_
		ystart=pnts[i]._height_;yend=pnts[i+1]._height_
		points.points[0]._offset_=xleft;points.points[0]._height_=ystart
		points.points[2]._offset_=xright;points.points[2]._height_=yend

		#calculate current dif
		startdif=0
		for k in range(xleft,xright):
			startdif+=abs(samples[k]-samplesorig[k])

		bestmatch=[startdif]+([None]*4)
		arc(True,True  ,xleft,xright,ystart,yend,bestmatch,samples,samplesorig)
		arc(True,False ,xleft,xright,ystart,yend,bestmatch,samples,samplesorig)
		arc(False,True ,xleft,xright,ystart,yend,bestmatch,samples,samplesorig)
		arc(False,False,xleft,xright,ystart,yend,bestmatch,samples,samplesorig)

		if bestmatch[0]!=startdif:
			points.points[0]._concav_=bestmatch[1];points.points[1]._concav_=bestmatch[2]
			points.points[1]._offset_=bestmatch[3];points.points[1]._height_=bestmatch[4]
			save.apply()

			pnts2[ix]._concav_=points.points[0]._concav_
			ix+=1
			pnts2.insert(ix,points.newp(points.points[1]._offset_,points.points[1]._height_,True,points.points[1]._concav_))
		else: #restore the line
			points.points[1]=points.points[2]
			points.points.pop()
			save.apply()
			points.points.insert(1,aux)
		ix+=1

		if print_test.get_active():
			testspack[0]+=bestmatch[0]
			for l in range(xleft,xright):
				testspack[1]+=abs(samplesorig[l])
			print(" "+str(i+1),end='',flush=True)  #+1? at least on 50 will be 1,2,...,49
			testspack[2]+=startdif    #again, for changes

		if pause.get_active():
			if ((i+2)%pause_after)==0:  #example: stop after 3, pase after 2, will stop at 2
				if (i+1)<sz: #not if was last
					if print_test.get_active():
						tests_phase2(pnts2,testspack,len(pnts)-(i+2))
					return (i+1,ix,False)
	if print_test.get_active():
		tests_phase2(pnts2,testspack,0)
	return (i,ix,True)

def fastsave(pack):
	fp=fastpath(True)
	with open(fp,"w") as f:
		pk=[points.serialize(pack[0]),points.serialize(pack[1])]+pack[2:] #pack is needed outside
		json.dump(pk,f)

def fastpath(is_save):
	f_in=play.entry.get_text()
	p=points.dpath(f_in)
	f=points.fpath(f_in,"fastresume")
	if is_save:
		pathlib.Path(p).mkdir(exist_ok=True)
		return f
	return os.path.exists(f)

def restore(b,combo):
	with open(fastpath(True)) as f:
		if d:=f.read():
			pack=json.loads(d)

			box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			box.append(sets.colorLabel("Fast Resume Continue"))

			print_test.get_parent().remove(print_test) #gtk critical without this
			pause.get_parent().remove(pause)
			bx=Gtk.Grid(hexpand=True)
			common_options(bx,0)
			box.append(bx)
			if not len(pack[7]):
				print_test.set_active(False)
				print_test.set_sensitive(False) #can't resume verbosity when was not
			else:
				print_test.set_active(True) #in case is not
			pause.set_active(True) #in case is not
			pause_points.set_text(str(pack[6]),-1)

			box.append(sets.colorButton("Continue",fastresumefn,"Start",[pack,combo]))
			combo[0].set_child(box)

def fastsavedone(b,bigpack):
	pack,combo=bigpack
	fastsave(pack)
	terminate(combo,pack[1],pack[3],pack[7])
def fastsaveresume(b,bigpack):
	pack,combo=bigpack
	fastsave(pack)
	resume(combo,pack)

def fastsavefinish():
	if fastpath(False):
		os.remove(fastpath(True))

def fastresumefn(b,bigpack):
	d=pause_points.get_text()
	dbool=d.isdigit()
	if dbool:
		d=int(d)
		if d<pause_points_minimum:
			pause_points.set_text(str(pause_points_minimum),-1)
		else:
			pack,combo=bigpack

			pack[6]=d
			if not print_test.get_sensitive():
				print_test.set_sensitive(True) #for another use at this
			elif not print_test.get_active():
				pack[7]=[] #user wants to unset verbosity from now

			points.points.clear()
			precalculate1()
			precalculate2()

			pack[0]=points.deserialize(pack[0])
			pack[1]=points.deserialize(pack[1])
			draw.samples=pack[2]

			waiter(combo,pack)
	else:
		pause_points.set_text(default_pause,-1)
