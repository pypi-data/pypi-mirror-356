
from gi.repository import Gtk
import json
import configparser

class colorLabel(Gtk.Label):
	def __init__(self,t,extratag=None):
		Gtk.Label.__init__(self)
		self._set_text_(t,extratag)
	def _set_text_(self,t,extratag=None):
		z="<span"#p is error
		if (c:=text_color.get_text()):
			z+=" color='"+c+"'"
		z+=">"
		if extratag: #can't set with Pango after.
			z+="<"+extratag+">"
		z+=t
		if extratag:
			z+="</"+extratag+">"
		z+="</span>"
		self.set_markup(z)
_click_ = "clicked"
class colorButton(Gtk.Button):
	def __init__(self,t,f,i,d=None):
		Gtk.Button.__init__(self,child=colorLabel(t))
		self.connect(_click_,f,d)
		self.set_tooltip_text(i)
	def _set_text_(self,t):
		self.get_child()._set_text_(t)
class colorEntry(Gtk.Entry):
	def __init__(self,b=Gtk.EntryBuffer()):
		Gtk.Entry.__init__(self,buffer=b,hexpand=True)
		self._color_()
	def _color_(self):
		if (c:=text_color.get_text()):
			cont=self.get_style_context()
			self._provider_=Gtk.CssProvider()
			self._provider_.load_from_data (b"entry { color: "+c.encode()+b"; }")
			cont.add_provider(self._provider_,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		else:
			self._provider_=None
	def _recolor_(self):
		if self._provider_:
			cont=self.get_style_context()
			cont.remove_provider(self._provider_)
		self._color_()

pkgname='audapa'
import appdirs
import os.path
import pathlib
from html import escape

from . import draw
from . import forms
from . import point

def get_config_dir():
	return pathlib.Path(appdirs.user_config_dir(pkgname))
def get_config_file():
	return os.path.join(get_config_dir(),'config.ini')

def get_data_dir():
	return pathlib.Path(appdirs.user_data_dir(pkgname))
def get_data_file(f):
	return os.path.join(get_data_dir(),f)

color=Gtk.EntryBuffer(text="purple")
def get_color():
	return color.get_text()
fgcolor=Gtk.EntryBuffer(text="red")
def get_fgcolor():
	return fgcolor.get_text()
fgcolor2=Gtk.EntryBuffer(text="green")
def get_fgcolor2():
	return fgcolor2.get_text()
fgcolor3=Gtk.EntryBuffer(text="blue")
def get_fgcolor3():
	return fgcolor3.get_text()
text_color=Gtk.EntryBuffer()
def get_text_color():
	return text_color.get_text()
turn_page=Gtk.CheckButton(active=True)
full_effect=Gtk.CheckButton(active=True)
def get_fulleffect():
	return full_effect.get_active()
distance=Gtk.EntryBuffer(text="10")
#(2*point.const).__str__() was good but will confilct with the example
cache_at_home=Gtk.CheckButton(active=False)

def add(bx,tx,x,n):
	return adder(bx,tx,colorEntry(x),n)
def adder(bx,tx,x,n):
	t=colorLabel(tx)
	t.set_halign(Gtk.Align.START)
	bx.attach(t,0,n,1,1)
	bx.attach(x,1,n,1,1)
	return n+1
def sets(b,combo):
	bx=Gtk.Grid(hexpand=True)
	n=add(bx,"Stroke Color",color,0)
	n=add(bx,"Foreground Color",fgcolor,n)
	n=add(bx,"Foreground Color2",fgcolor2,n)
	n=add(bx,"Foreground Color3",fgcolor3,n)
	n=add(bx,"Text Color",text_color,n)
	n=adder(bx,"Turn the page at margin touch",turn_page,n)
	n=adder(bx,forms.formal_write+" after a points effect",full_effect,n)
	n=add(bx,"Minimum distance between points",distance,n)
	n=adder(bx,"Cache dir for points in home folder",cache_at_home,n)
	b=colorButton("Done", reset, "Return", {'c':combo,'t':
		{'cl':color.get_text(),'fcl':fgcolor.get_text()}})
	bx.attach(b,0,n,2,1)
	combo[0].set_child(bx)

def init():
	get_config_dir().mkdir(exist_ok=True)
	get_data_dir().mkdir(exist_ok=True)
	config = configparser.ConfigParser()
	if(config.read(get_config_file())):
		c=config['conf']
		init_t(c,'color',color)
		init_t(c,'fgcolor',fgcolor)
		init_t(c,'fgcolor2',fgcolor2)
		init_t(c,'fgcolor3',fgcolor3)
		init_t(c,'text_color',text_color)
		init_c(c,'turn',turn_page)
		init_c(c,'effect',full_effect)
		init_t(c,'distance',distance)
		init_c(c,'homecache',cache_at_home)
def init_t(src,key,dst):
	if key in src: #this is not checking values
		dst.set_text(src[key],-1)
def init_c(src,key,dst):
	if key in src:
		dst.set_active(False if src[key]=='False' else True)

def reset(b,di):
	config = configparser.ConfigParser()
	config['conf']={}
	c=config['conf']
	c['color']=color.get_text()
	c['fgcolor']=fgcolor.get_text()
	c['fgcolor2']=fgcolor2.get_text()
	c['fgcolor3']=fgcolor3.get_text()
	c['text_color']=text_color.get_text()
	c['turn']=turn_page.get_active().__str__()
	c['effect']=full_effect.get_active().__str__()
	c['distance']=distance.get_text()
	c['homecache']=cache_at_home.get_active().__str__()
	with open(get_config_file(), "w") as configfile:
		config.write(configfile)
	win=di['c'][0]
	box=di['c'][1]
	if di['t']['cl']==c['color']:
		win.set_child(box)
		if di['t']['fcl']!=c['fgcolor']:
			draw.draw_sel()
		return
	draw.reset()
	search(box)
	win.set_child(box)
def search(p):
	x=p.get_first_child()
	while x:
		if isinstance(x,colorLabel):
			x._set_text_(escape(x.get_text()))
		elif isinstance(x,colorEntry):
			x._recolor_()
		else:
			search(x)
		x=x.get_next_sibling()
