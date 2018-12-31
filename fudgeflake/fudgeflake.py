from PIL import Image,ImageDraw

w=1000
h=1000
s=3**-0.5

def terdragon(draw,x0,y0,h0,x3,y3,h3):
    if ((x3-x0)*(x3-x0)+(y3-y0)*(y3-y0))<1: return
    x1=(x0+x3+s*(y3-y0))/2
    y1=(y0+y3+s*(x0-x3))/2
    h1=(2*h0+h3)/3
    x2=(x0+x3-s*(y3-y0))/2
    y2=(y0+y3-s*(x0-x3))/2
    h2=(h0+2*h3)/3
    draw.point((x1,y1),fill='hsl(%d,100%%,50%%)'%(h1*360))
    draw.point((x2,y2),fill='hsl(%d,100%%,50%%)'%(h2*360))
    terdragon(draw,x0,y0,h0,x1,y1,h1)
    terdragon(draw,x1,y1,h1,x2,y2,h2)
    terdragon(draw,x2,y2,h2,x3,y3,h3)

def fudgeflake():
    im=Image.new('RGB',(w,h))
    draw=ImageDraw.Draw(im)
    terdragon(draw,900,500,0.0,300,154,1.0/3)
    terdragon(draw,300,154,1.0/3,300,846,2.0/3)
    terdragon(draw,300,846,2.0/3,900,500,1.0)
    return im
