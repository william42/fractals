from PIL import Image,ImageDraw
from cmath import phase
from math import pi

ph1=0.6180339887498948
ph2=0.3819660112501051
w10=(0.8090169943749475+0.5877852522924731j)
aspect=0.3632712640026804 #aspect ratio of the gnomon laid flat

def line(draw,z1,z2):
    draw.line((z1.real,z1.imag,z2.real,z2.imag),fill='black')

def colorin(draw,z1,z2,z3):
    c='hsl(%d,100%%,50%%)'%((phase(z1-z3)+pi)*360/pi)
    draw.polygon((z1.real,z1.imag,z2.real,z2.imag,z3.real,z3.imag)
        ,outline=c,fill=c)

def gnomon(draw,z1,z2,z3,n):
    #if n<=0: return
    if n<=0:
        #colorin(draw,z1,z2,z3)
        return
    zn=ph1*z1+ph2*z3
    line(draw,zn,z2)
    gnomon(draw,z2,zn,z1,n-2)
    triangle(draw,z2,z3,zn,n-1)

def triangle(draw,z1,z2,z3,n):
    #if n<=0: return
    if n<=0:
        #colorin(draw,z1,z2,z3)
        return
    zn=ph1*z1+ph2*z2
    line(draw,zn,z3)
    triangle(draw,zn,z3,z1,n-2)
    gnomon(draw,z2,zn,z3,n-1)

def robinson(w,n):
    h = w * aspect
    z1=h*1j
    z2=w/2
    z3=w+z1
    #im=Image.new('RGB',(w,int(h)))#,'white')
    im=Image.new('RGB',(w,int(h)),'white')
    draw=ImageDraw.Draw(im)
    line(draw,z1,z2)
    line(draw,z2,z3)
    line(draw,z3,z1)
    gnomon(draw,z1,z2,z3,n)
    return im
    
def decagon(w,n):
    s=w/2
    c=s*(1+1j)
    m=s
    im=Image.new('RGB',(w,w))
    draw=ImageDraw.Draw(im)
    for i in xrange(5):
        z1=c+m
        m*=w10
        z2=c+m
        m*=w10
        z3=c+m
        triangle(draw,z1,c,z2,n)
        triangle(draw,z3,c,z2,n)
    return im
    
