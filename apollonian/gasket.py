from PIL import Image,ImageDraw

def addcircles(c1,c2):
    k1,kx1,ky1=c1
    k2,kx2,ky2=c2
    k=k1+k2
    kx=kx1+kx2
    ky=ky1+ky2
    return k,kx,ky

def tangency(c1,c2):
    k,kx,ky=addcircles(c1,c2)
    x=kx/k
    y=ky/k
    return x,y
    
def shift(s,p):
    x,y=p
    return (s-0.5)*(1+x),(s-0.5)*(1+y)
    
def line(draw,s,p1,p2):
    draw.line((shift(s,p1),shift(s,p2)),fill='black')

def triangle(draw,s,c1,c2,c3,count,im):
    p1=tangency(c1,c2)
    p2=tangency(c2,c3)
    p3=tangency(c3,c1)
    line(draw,s,p1,p2)
    line(draw,s,p2,p3)
    line(draw,s,p3,p1)
    if count%10==1: im.save('frame%05d.png'%count)
    return count+1
    

def newtangent(pc,c):
    return tuple([2*pc[i]-3*c[i] for i in range(3)])

def triangulum(draw,s,c0,c1,c2,c3,count,im):
    if c1[0]+c2[0]+c3[0]>2*s:
        return triangle(draw,s,c1,c2,c3,count,im)
    pc=addcircles(addcircles(c0,c1),addcircles(c2,c3))
    count=triangulum(draw,s,newtangent(pc,c3),c2,c1,c0,count,im)
    count=triangulum(draw,s,newtangent(pc,c2),c1,c0,c3,count,im)
    return triangulum(draw,s,newtangent(pc,c1),c0,c3,c2,count,im)

def pregasket(draw,s,c0,c1,c2,c3,im):
    count=triangulum(draw,s,c3,c1,c0,c2,0,im)
    c4=newtangent(addcircles(addcircles(c0,c1),addcircles(c2,c3)),c3)
    return triangulum(draw,s,c4,c2,c0,c1,count,im)

def gasket(s):
    im=Image.new('RGB',(2*s,2*s),'white')
    count=pregasket(ImageDraw.Draw(im),s,
                    (-1.0,0.0,0.0),
                    (2.0,-1.0,0.0),
                    (2.0,1.0,0.0),
                    (3.0,0.0,2.0),im)
    im.save('frame00000.png')
    for i in range(10):
        im.save('frame1%04d.png'%i)
    return im


