#!/usr/bin/env python

from cmath import pi
from sys import argv
import cairo

#WIDTH, HEIGHT = 3000, 1500
WIDTH, HEIGHT = 851, 315

if len(argv)>=5:
    k1,k2,k3,k4=[int(x) for x in argv[1:5]]
else:
    k1,k2,k3,k4=-1,2,2,3

if k1>0:
    raise ArithmeticError('The first curvature must be <= zero')

des=2*(k1*k1+k2*k2+k3*k3+k4*k4)-(k1+k2+k3+k4)**2
if des!=0:
    raise ArithmeticError('Invalid Apollonian gasket(Descartes theorem violation)')

limit = 400*max(-k1,1)
#text_limit = 1000
text_limit=100

filename='{},{},{},{}'.format(k1,k2,k3,k4)

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
#surface = cairo.SVGSurface(filename+'.svg', WIDTH, HEIGHT)
ctx = cairo.Context (surface)

def circle(a):
    z,k = a
    r=1/k
    z=z*r
    ctx.arc(z.real,z.imag,abs(r),0,2*pi)
    ctx.stroke()
    if k<0: return
    if k>text_limit: return
    if k<100:
        ctx.set_font_size(r)
    else:
        ctx.set_font_size(2*r/3)
    ks=str(k)
    xbearing, ybearing, kwidth, kheight, xadvance, yadvance = (ctx.text_extents(ks))
    ctx.move_to(z.real - xbearing - kwidth / 2, z.imag - ybearing - kheight / 2)
    ctx.show_text(ks)
    ctx.stroke()

def altcirc(a1,a2,a3,a4):
    z1,k1=a1
    z2,k2=a2
    z3,k3=a3
    z4,k4=a4
    return 2*(z2+z3+z4)-z1,2*(k2+k3+k4)-k1

def arb(a1,a2,a3,a4):
    a1a=altcirc(a1,a2,a3,a4)
    circle(a1a)
    if a1a[1]>limit: return
    arb(a2,a1a,a3,a4)
    arb(a3,a2,a1a,a4)
    arb(a4,a2,a3,a1a)

def gasketa(a1,a2,a3,a4):
    circle(a1); arb(a1,a2,a3,a4)
    circle(a2); arb(a2,a3,a4,a1)
    circle(a3); arb(a3,a4,a1,a2)
    circle(a4); arb(a4,a1,a2,a3)

def belt():
    ctx.set_source_rgb(1,1,1)
    ctx.rectangle(-3,-1,6,2)
    ctx.fill()
    ctx.set_source_rgb(0,0,0)
    ctx.move_to(-3,-1)
    ctx.line_to(3,-1)
    ctx.move_to(-3,1)
    ctx.line_to(3,1)
    ctx.stroke()
    l1=(1j,0)
    l2=(-1j,0)
    c1=(-3,1)
    c2=(-1,1)
    c3=(1,1)
    c4=(3,1)
    circle(c1); circle(c2); circle(c3); circle(c4);
    arb(l1,l2,c1,c2); arb(l2,l1,c1,c2)
    arb(l1,l2,c2,c3); arb(l2,l1,c2,c3)
    arb(l1,l2,c3,c4); arb(l2,l1,c3,c4)

def gasket(k1,k2,k3,k4):
    if (k1==0):
        belt()
        return
    #note: assuming a proper gasket, k1<0
    h=(k1+k2+k3+k4)/2
    l3=h-k3
    l4=h-k4
    z1=0
    z2=(k1+k2)/(k1)
    z3=(complex(l4,k1)**2)/((k1+k2)*k1)
    z4=(complex(l3,-k1)**2)/((k1+k2)*k1)
    ctx.set_source_rgb(1,1,1)
    ctx.arc(0,0,1,0,2*pi)
    ctx.fill()
    ctx.set_source_rgb(0,0,0)
    ctx.scale(-k1,-k1)
    gasketa((z1,k1),(z2,k2),(z3,k3),(z4,k4))

ctx.translate(WIDTH/2,HEIGHT/2)
ctx.scale(HEIGHT/2-10,HEIGHT/2-10)

ctx.set_line_width (0.003/max(-k1,1))


#gasket(-1,2,2,3)
#gasket(-2,3,6,7)
gasket(k1,k2,k3,k4)

#surface.write_to_png(filename+".png")
surface.write_to_png("cover.png")
#surface.finish()
