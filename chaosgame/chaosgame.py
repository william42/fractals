from PIL import Image,ImageDraw
from random import randint

#w=1100
#h=600
#origin=100+300j
w=1920
h=1080
origin=174+540j
a=(-0.5+0.8660254037844386j)
b=2+a
shift=0,1/b,(1+a)/b
scale=1/b,a/b,1/b

def plot(draw,z,h):
    #w = 900*z+origin
    w=1571*z+origin
    draw.point((w.real,w.imag),fill='hsl(%d,100%%,50%%)'%(h*360))

def chaosgame1(draw,n):
    z=0+0j
    h=0.0
    for i in xrange(n):
        plot(draw,z,h)
        j=randint(0,2)
        z=z*scale[j]+shift[j]
        h=(h+j)/3

def chaosgame(n):
    im = Image.new('RGB',(w,h))
    draw = ImageDraw.Draw(im)
    chaosgame1(draw,n)
    return im
