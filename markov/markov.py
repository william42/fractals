#!/usr/bin/env python

from math import log,exp,pi
import cairo

WIDTH, HEIGHT = 1000, 1000
radius=0.2

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
#surface = cairo.SVGSurface(filename+'.svg', WIDTH, HEIGHT)
ctx = cairo.Context (surface)

def plot(x,y,z):
    cx=log(x)-.5*(log(y)+log(z))
    cy=0.8660254037844386*(log(y)-log(z))
    ctx.arc(cx,cy,radius,0,2*pi)
    ctx.fill()

def plot3(x,y,z):
    #one cycle
    plot(x,y,z)
    plot(y,z,x)
    plot(z,x,y)

def point(x,y,z):
    plot3(x,y,z)
    plot3(y,x,z)

def treefrom(limit,x,y,z):
    point(x,y,z)
    if z>=limit: return
    treefrom(limit,x,z,3*x*z-y)
    treefrom(limit,y,z,3*y*z-x)

def markov(limit):
    ctx.set_source_rgb(1,1,1)
    ctx.paint()
    ctx.fill()
    ctx.set_source_rgb(0,0,0)
    plot(1,1,1)
    plot3(1,1,2)
    treefrom(limit,1,2,5)

ctx.translate(WIDTH/2,HEIGHT/2)
ctx.scale(WIDTH/(2*60),HEIGHT/(2*60))

markov(exp(120))

surface.write_to_png("markov.png")
#surface.finish()
