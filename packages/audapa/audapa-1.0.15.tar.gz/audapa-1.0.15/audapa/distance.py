
import math

import decimal
decimal.getcontext().prec=1
decimal.getcontext().rounding = decimal.ROUND_DOWN

from . import draw
from . import sets
from . import point
from . import points
from . import pbox

def test(x,y,p):
	d=float(sets.distance.get_text())
	if d:
		a=draw.cont.get_last_child() #iterate from last to first
		return recurse(x,y,p,a,d)
	return True

def check(a,b,d):
	x=a[0]+point.const-b[0]
	y=a[1]+point.const-b[1]
	c=math.sqrt(pow(x,2)+pow(y,2))
	if c<d: #<= can be another way
		e=decimal.Decimal(c%1)
		return int(c)+e.normalize().__float__()
	return -1

def recurse(x,y,p,a,d):
	if a:
		if a!=p:
			c=check(draw.cont.get_child_position(a),[x,y],d)
			if c!=-1:
				print(c.__str__()+" is less than the minimum required distance of "+d.__str__())
				return False
		return recurse(x,y,p,a.get_prev_sibling(),d)
	return True

def test_all():
	sz=len(points.points)
	if sz:
		d=float(sets.distance.get_text())
		a=points.points[0]._coord_(draw.wstore,draw.hstore)
		for i in range(1,sz):
			p=points.points[i]
			b=p._coord_(draw.wstore,draw.hstore)
			c=check(a,b,d)
			if c!=-1:
				return (p,c)
			a=b
	return None

def hold(p,b,f,d):
	if not b:
		b=sets.colorButton(text(p),f,"Confirm",d)
		return b
	b._set_text_(text(p))
	return b
def text(z):
	return "Distance problem at "+pbox.inf(z[0])+": "+z[1].__str__()
