from PIL import Image,ImageDraw

w=1200
h=600

def koch1(draw,s,x0,y0,h0,x2,y2,h2):
    if ((x2-x0)*(x2-x0)+(y2-y0)*(y2-y0))<1: return
    x1=(x0+x2+s*(y2-y0))/2
    y1=(y0+y2+s*(x0-x2))/2
    h1=(h0+h2)/2
    draw.point((x1,y1),fill='hsl(%d,100%%,50%%)'%(h1*360))
    koch1(draw,s,x2,y2,h2,x1,y1,h1)
    koch1(draw,s,x1,y1,h1,x0,y0,h0)

def koch(s):
    im = Image.new('RGB',(w,h))
    draw = ImageDraw.Draw(im)
    koch1(draw,s,0.0,h-1,0.0,w-1,h-1,1.0)
    return im

def kochs():
    for i in xrange(201):
        koch(i/200.0).save('frame%04d.png'%i)
