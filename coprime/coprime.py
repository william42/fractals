#!/usr/bin/env python

from math import log,exp,pi
import cairo

WIDTH, HEIGHT = 1000, 1000
radius=0.2

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
#surface = cairo.SVGSurface(filename+'.svg', WIDTH, HEIGHT)
ctx = cairo.Context (surface)

def plot(x,y):
    cx=x-.5*y
    cy=0.8660254037844386*y
    ctx.arc(cx,cy,radius,0,2*pi)
    ctx.fill()

def point(x,y):
    plot(x,y)
    plot(x,-y)
    plot(-x,y)
    plot(-x,-y)

def treefrom(limit,x,y):
    point(x,y)
    if (x+y)>=limit: return
    treefrom(limit,x+y,y)
    treefrom(limit,x,x+y)

def markov(limit):
    ctx.set_source_rgb(1,1,1)
    ctx.paint()
    ctx.fill()
    ctx.set_source_rgb(0,0,0)
    treefrom(limit,1,1)

ctx.translate(WIDTH/2,HEIGHT/2)
ctx.scale(WIDTH/(2*60),HEIGHT/(2*60))

markov(120)

surface.write_to_png("coprime.png")
#surface.finish()
