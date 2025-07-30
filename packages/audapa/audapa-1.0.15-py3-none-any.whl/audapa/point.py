
from gi.repository import Gtk,Gdk,GLib

from . import sets
from . import draw
from . import drawscroll
from . import pbox
from . import points
from . import graph
from . import arcbutton
from . import distance

const=6 #this is the radius
default_concav=True

class struct(Gtk.DrawingArea):
	_drag_=False
	#offset,height,inter,concav
	#                    here is like the Arc Orientation button that at start is /\ that is concav
	#                    https://math.stackexchange.com/questions/2364116/how-to-remember-which-function-is-concave-and-which-one-is-convex
	#control
	def __init__(self,*args):
		Gtk.DrawingArea.__init__(self)
		self._control_ = Gtk.GestureClick()
		self._control_.connect("pressed",self._press_,None)
		self.add_controller(self._control_)
		self.set_size_request(2*const,2*const)
		if len(args)==0:
			self.set_draw_func(self._draw_none_,None,None)
			return
		self._inter_=False
		self._concav_=default_concav
		self._pos_(args[0],args[1])
		ix=points.insert(self)
		puts,dels=self._take_(ix)
		w=draw.wstore
		h=draw.hstore
		graph.lines(dels,puts,w,h)
		self._put_point_(w,h)
		self._control_.emit("pressed",0,0,0)
	def _take_(self,ix):
		if a:=graph.take(ix,self):
			if len(a)==2:
				return (a,[[a[0][0],a[1][1]]])
			return (a,[])
		return ([],[])
	def _pos_(self,x,y):
		if drawscroll.landscape:
			o=x
			h=draw.sampsize*y/draw.hstore
		else:
			o=y
			h=draw.sampsize*x/draw.wstore
		self._offset_=int(draw.offset+o)
		self._height_=int(h-(draw.sampsize*draw.baseline))
	def _color_(self):
		if self._inter_==False:
			return sets.get_fgcolor2()
		return sets.get_fgcolor3()
	def _draw_none_(self,widget,cr,width,height,d,u):
		co=Gdk.RGBA()
		if co.parse(self._color_()):
			cr.set_source_rgb(co.red,co.green,co.blue)
		if self._drag_:
			cr.arc(const,const,const,0,2*GLib.PI)
		else:
			cr.rectangle(0,0,width,height)
		cr.stroke()
	def _draw_cont_(self,widget,cr,width,height,d,u):
		co=Gdk.RGBA()
		if co.parse(self._color_()):
			cr.set_source_rgb(co.red,co.green,co.blue)
		if self._drag_:
			cr.arc(const,const,const,0,2*GLib.PI)
		else:
			cr.rectangle(0,0,width,height)
		cr.fill()
	def _put_(self,w,h,ix):
		graph.put(ix,self,w,h)
		c=self._coord_(w,h)
		draw.cont.put(self,c[0]-const,c[1]-const)
	def _put_point_(self,w,h):
		c=self._coord_(w,h)
		draw.cont.put(self,c[0]-const,c[1]-const)
	def _coord_(self,w,h):
		z=self._offset_-draw.offset
		if drawscroll.landscape:
			y=self._height_*h/draw.sampsize
			y+=h*draw.baseline
			return [z,y]
		y=self._height_*w/draw.sampsize
		y+=w*draw.baseline
		return [y,z]
	def _press_(self,a,n,x,y,d):
		global lastselect
		if lastselect:
			if lastselect!=self:
				lastselect.set_draw_func(lastselect._draw_none_,None,None)
				self._info_()
				arcbutton.button._set_text_(arcbutton.set(self))
			else:
				if self._drag_==False:
					self._drag_=True
				else:
					self._drag_=False
				self.queue_draw()
				return
		else:
			pbox.open(self)
		lastselect=self
		self.set_draw_func(self._draw_cont_,None,None)
	def _dend_(self,x,y):
		if distance.test(x,y,self):
			w=draw.wstore
			h=draw.hstore
			#
			ini=points.points.index(self)
			if dels:=graph.take(ini,self):
				graph.dels(dels,w,h)
			#
			o=self._offset_
			self._pos_(x,y)
			if puts:=points.move(self,o,ini,dels):
				graph.lines(dels,puts,w,h)
			if self.get_parent():
				c=self._coord_(w,h)
				draw.cont.move(self,c[0]-const,c[1]-const)
			else:
				self._put_point_(w,h)
			self._info_()
	def _remove_(self,ix):
		self.remove_controller(self._control_)
		del points.points[ix]
	def _info_(self):
		pbox.info._set_text_(pbox.inf(self))
