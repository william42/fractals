#!/usr/bin/env python
from cmath import log,pi
import cairo

width,height=1920,1080

omega=-0.5+0.8660254037844387j
omega2=omega.conjugate()


surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)


ctx.set_source_rgb(1,1,1)
ctx.rectangle(0,0,width,height)
ctx.fill()
ctx.set_source_rgb(0,0,0)

ctx.translate(0,height/2)
ctx.scale(height*1.0/(pi),height*1.0/(pi))
ctx.set_line_width(2.0/width)



def logline(z1,z2):
    u=log(z1); v=log(z2)
    if abs(u.imag-v.imag)>pi: return
    ctx.move_to(u.real,u.imag)
    ctx.line_to(v.real,v.imag)

for i in range(-300,300):
    for j in range(-300,300):
        z=i+j*omega
        z*=(omega+2)
        logline(z+1,z+2)
        logline(z+omega,z+2*omega)
        logline(z+omega2,z+2*omega2)
        #add two more
        ctx.stroke()

surface.write_to_png("loghexes.png")

