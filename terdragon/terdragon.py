#!/usr/bin/env python2
from PIL import Image,ImageDraw
from cmath import exp
from math import pi

w=1366
h=768

def counter(im):
    i=0
    while True:
        for j in xrange(1000):
            yield
        i+=1
        im.save('frame%04d.png'%i)

def plot(draw,z,h):
    draw.point((z.real,z.imag),fill='hsl(%d,100%%,50%%)'%(h*360))

def terdragon1(c,draw,a,z0,h0,z3,h3):
    if abs(z0-z3)<1: return
    z1=(1-a)*z0+a*z3
    z2=a*z0+(1-a)*z3
    h1=(2*h0+h3)/3
    h2=(h0+2*h3)/3
    terdragon1(c,draw,a,z0,h0,z1,h1)
    plot(draw,z1,h1)
    terdragon1(c,draw,a,z1,h2,z2,h1)
    plot(draw,z2,h2)
    terdragon1(c,draw,a,z2,h2,z3,h3)
    c.next()

def terdragon(theta):
    im=Image.new('RGB',(w,h))
    draw=ImageDraw.Draw(im)
    z0=w/11+(h/2)*1j
    z1=10*w/11+(h/2)*1j
    plot(draw,z0,0)
    plot(draw,z1,1)
    c=counter(im)
    a=(2-exp(theta*1j))/3
    terdragon1(c,draw,a,z0,0.0,z1,1.0)
    for j in xrange(10000):
        c.next()
    return im

def terdragons():
    for i in xrange(201):
        terdragon(pi*i/600).save("frame%04d.png"%i)


terdragon(pi/3).save("ter-dyre.png")
