import numpy as np
from PIL import Image
import datetime;
import subprocess

sizeX = 512
sizeY = 512

repeat = 0

permutation = np.random.randint(low=0,high=255,size=[256],dtype=np.uint16)
p = np.empty([sizeX],dtype=np.uint16)

i = 0
while(i < 512):
    p[i] = permutation[i%256]
    i += 1
    

def fade(t):
    #6t^5 - 15t^4 + 10t^3
    return ((t*t*t)*((t*t*6) - (t*15) + (10)))
    
def grad(h, x, y, z):
    #print("grad x: {0} y: {1}".format(x,y))
    z = h & 0xF
    if(z == 0x0):
        return  x + y
    if(z == 0x1):
        return -x + y
    if(z == 0x2):
        return  x - y
    if(z == 0x3):
        return -x - y
    if(z == 0x4):
        return  x + z
    if(z == 0x5):
        return -x + z
    if(z == 0x6):
        return  x - z
    if(z == 0x7):
        return -x - z
    if(z == 0x8):
        return  y + z
    if(z == 0x9):
        return -y + z
    if(z == 0xA):
        return  y - z
    if(z == 0xB):
        return -y - z
    if(z == 0xC):
        return  y + x
    if(z == 0xD):
        return -y + z 
    if(z == 0xE):
        return  y - x
    if(z == 0xF):
        return -y - z
        
def lerp(a, b, x):
    #print("inputs: a:{0} b:{1} x:{2}".format(a,b,x))
    out = a+x*(b-a)
    return out
    
    
def perlin(x, y, z=0):

    xi = int(np.floor(x)) & 255
    yi = int(np.floor(y)) & 255
    zi = int(np.floor(z)) & 255
    
    x = x - np.floor(x)
    y = y - np.floor(y)
    z = z - np.floor(z)
    u = fade(x)
    v = fade(y)
    w = fade(z)
        
    a =  p[xi]  + yi
    aa = p[a]   + zi
    ab = p[a+1] + zi
    b =  p[xi+1]+ yi
    ba = p[b]   + zi
    bb = p[b+1] + zi
    
    l1a = lerp(grad(p[aa  ], x  , y  ,  z), 
               grad(p[ba  ], x-1, y  ,  z), u)
    l1b = lerp(grad(p[ab  ], x  , y-1,  z),
               grad(p[bb  ], x-1, y-1,  z), u)
              
    l2a = lerp(grad(p[aa+1], x  , y  ,  z-1), 
               grad(p[ba+1], x-1, y  ,  z-1), u)
    l2b = lerp(grad(p[ab+1], x  , y-1,  z-1),
               grad(p[bb+1], x-1, y-1,  z-1), u)
    
    l1 = lerp(l1a,l1b,v)
    l2 = lerp(l2a,l2b,v)
    
    return (lerp(l1, l2, w))
    
picSizeX = 1000 #1000
picSizeY = 1400 #1400

desiredMax = 300.#30.12
interval = desiredMax / picSizeX
print(interval)
    
#make array 

#temp = np.random.randint(low=0,high=255,size=[picSizeX,picSizeY,3],dtype=np.uint16)
temp = np.empty([picSizeX,picSizeY,3])

if(False):
    i = 0
    while(i < picSizeX):
        print(i)
        ii = 0
        while(ii < picSizeY):
            tr = np.random.random()*0.1 #*(2*i/picSizeX)
            pout = perlin((i-(picSizeX/2))*(interval*(1+tr)),(ii-(picSizeY/2))*(interval*(1+tr)))
            pout = (pout*10 + 255/2)
            if(pout < 150):
                pout = 0
            if(pout > 255):
                pout = 255
            #print(int(pout))
            temp[i,ii,0] = 0
            temp[i,ii,1] = 0
            temp[i,ii,2] = pout
            ii += 1
        i += 1

print(temp.shape)


#clear out center
center = np.asarray([picSizeX/2,picSizeY/2])

if(False):
    i = 0
    while(i < picSizeX):
        print(i)
        ii = 0
        while(ii < picSizeY):
            if(np.linalg.norm(center-np.asarray([i,ii])) < 400+0.5+50+50):
                temp[i,ii,0] = 0
                temp[i,ii,1] = 0
                temp[i,ii,2] = 0
            ii += 1
        i += 1
  
#noise to black by distance to center 
if(False):
    i = 0
    while(i < picSizeX):
        print(i)
        ii = 0
        while(ii < picSizeY):
            dist = np.linalg.norm(center-np.asarray([i,ii]))
            #normalize to 0,1
            r = picSizeY - 0
            a = (dist - 0) / r
            if(np.random.random() > a):
                temp[i,ii,0] = 0
                temp[i,ii,1] = 0
                temp[i,ii,2] = 0
            ii += 1
        i += 1  
       
#white to black by distance to center 
if(False):
    i = 0
    while(i < picSizeX):
        print(i)
        ii = 0
        while(ii < picSizeY):
            dist = np.linalg.norm(center-np.asarray([i,ii]))
            #normalize to 0,1
            r = picSizeY - 0
            a = (dist - 0) / r
            #scale to [0,255]
            r2 = 255 - 0
            a = (a * r2) + 0
            temp[i,ii,0] = a
            temp[i,ii,1] = a
            temp[i,ii,2] = a
            ii += 1
        i += 1

#draw ring

def xfun(x,y,t,z):
    return x+(400-z*4)*np.cos(t*30)
    
def yfun(x,y,t,z):
    return y+(400-z*4)*np.sin(t*30)

#center the starting point
x = picSizeX/2
y = picSizeY/2
 
 
if(False):
    #draw
    t = 0
    tMax = 800
    stepSize = 0.5
    while(t < tMax):
        i = 0
        while(i < 100):
            xt = xfun(x,y,t,i)
            yt = yfun(x,y,t,i)
            #xt = xfun(x+((np.random.random()-0.5)*5),y,t,i)
            #yt = yfun(x,y+((np.random.random()-0.5)*5),t,i)
            if(xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
                ixt = int(xt)
                iyt = int(yt)
                temp[ixt,iyt,0] = (t / tMax)*255
                temp[ixt,iyt,1] = ((tMax-t) / tMax)*255
                temp[ixt,iyt,2] = 55#(t / tMax)*255
            i += 1
        print("t:{0}\n".format(t))
        t += np.random.random()*stepSize
    
    
def xfun(x,y,t,z):
    return x+(450.25)*np.cos(t*30)+50*np.cos(t*5)
    
def yfun(x,y,t,z):
    return y+(450.25)*np.sin(t*30)+50*np.sin(t*5)

if(False):
    #draw
    t = 0
    tMax = 800*4
    stepSize = 0.05
    while(t < tMax):
        i = 0
        while(i < 1):
            xt = xfun(x,y,t,i)
            yt = yfun(x,y,t,i)
            if(xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
                ixt = int(xt)
                iyt = int(yt)
                temp[ixt,iyt,0] = (t / tMax)*255
                temp[ixt,iyt,1] = 255
                temp[ixt,iyt,2] = 55#(t / tMax)*255
            i += 1
        print("t:{0}\n".format(t))
        t += np.random.random()*stepSize
    
    
def xfun(x,y,t,z):
    return x+(1*z)*np.cos(np.radians(t))
    
def yfun(x,y,t,z):
    return y+(1*z)*np.sin(np.radians(t))
    
def xfun2(x,y,t,z):
    return x+(5+z)*np.cos(np.radians(t))
    
def yfun2(x,y,t,z):
    return y+(5+z)*np.sin(np.radians(t))

golden_ratio = 1.61803398875

if(False):
    z = 0
    while(z < 1):
        #draw
        ringCount = 1
        ringTimer = 0.
        t = 0
        tMax = 360*1000
        stepSize = 1.
        while(t < tMax):
            xt = xfun(x,y,t,ringCount)
            yt = yfun(x,y,t,ringCount)
            if(False and xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
                ixt = int(xt)
                iyt = int(yt)
                temp[ixt,iyt,0] = 200
                temp[ixt,iyt,1] = 0
                temp[ixt,iyt,2] = 255#(t / tMax)*255
            
            if(ringTimer > 360/golden_ratio):
                print("ring {0}".format(ringCount))
                ringCount += 1
                ringTimer = 0.
                i = 0
                while(i < 360):
                    xt2 = xfun2(xt,yt,i,ringCount)
                    yt2 = yfun2(xt,yt,i,ringCount)
                    if(xt2 < picSizeX and xt2 >= 0 and yt2 < picSizeY and yt2 >= 0):
                        ixt2 = int(xt2)
                        iyt2 = int(yt2)
                        dist = np.linalg.norm(center-np.asarray([ixt2,iyt2]))
                        #normalize to 0,1
                        r = 300
                        a = (dist - 0) / r
                        #scale to [0,255]
                        r2 = 255 - 0
                        a = (a * r2) + 0
                        a2 = a
                        if(a > 255):
                            a = 255
                        temp[ixt2,iyt2,0] = 255 - a
                        temp[ixt2,iyt2,2] = 255 - a
                        if(255 - a2/1.5 < 0):
                            temp[ixt2,iyt2,0] = 255
                        else:
                            temp[ixt2,iyt2,1] = 255 - a2/1.5
                        
                    i += 0.05
            #print("t:{0}\n".format(t))
            ringTimer += stepSize
            t += stepSize
        z += 1
        
def xfun(x,y,t,z):
    return x+(450.25-((450.25/100)*z))*np.cos(np.radians(t/4))
    
def yfun(x,y,t,z):
    return y+(0-(4*z))*np.sin(np.radians(t/4))        

if(False):
    z = 0
    while(z < 100):
        print ("eye {0}".format(z))
        t = 0
        tMax = 360*4
        stepSize = 1.
        while(t < tMax):
            xt = xfun(x+(np.random.random()-1)*20,y,t,z)
            yt = yfun(x,y+(np.random.random()-1)*20,t,z)
            if(xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
                ixt = int(xt)
                iyt = int(yt)
                temp[ixt,iyt,0] = 0
                temp[ixt,iyt,1] = 0
                temp[ixt,iyt,2] = 255#(t / tMax)*255
            t += stepSize
        z += 1
        
#black pupil
center = np.asarray([picSizeX/2,picSizeY/2])

if(False):
    i = int(picSizeX/2 - 100)
    while(i < int(picSizeX/2 + 100)):
        print(i)
        ii = int(picSizeY/2 - 100)
        while(ii < int(picSizeY/2 + 100)):
            if(np.linalg.norm(center-np.asarray([i,ii])) < 10):
                temp[i,ii,0] = 0
                temp[i,ii,1] = 0
                temp[i,ii,2] = 0
            ii += 1
        i += 1

def xfun(x,y,t,z):
    return x+((360*4)/(z*4))*np.cos(np.radians(t/4))
    
def yfun(x,y,t,z):
    return y+((360*4)/(z*4))*np.sin(np.radians(t/4))        
    
    
def drawCircle(x,y,z,level):
    #print("\tcircle")
    t = 0
    tMax = 360*4
    stepSize = 1.
    while(t < tMax):
        xt = xfun(x,y,t,level)
        yt = yfun(x,y,t,level)
        if(xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
            ixt = int(xt)
            iyt = int(yt)
            temp[ixt,iyt,0] = 0
            temp[ixt,iyt,1] = 0
            temp[ixt,iyt,2] = 255#(t / tMax)*255
        t += stepSize
    if(level < 3):
        recursive(x,y,level+1)

def recursive(x,y,level):
    o = ""
    i = 1
    while(i < level):
        o = o + "\t"
        i += 1
    print ("{0}circles level {1}".format(o,level))
    z = 0 #unused currently
    x = x - (360/(level*4*2))
    y = y - (360/(level*4*2))
    drawCircle(x,y,z,level)
    drawCircle(x+(360/(level*4)),y,z,level)
    drawCircle(x,y+(360/(level*4)),z,level)
    drawCircle(x+(360/(level*4)),y+(360/(level*4)),z,level)
    
    
        
if(True):
    level = 1
    recursive(x,y,level) 


# convert array to Image
img = Image.fromarray(temp.astype('uint8'))
img.save("perlin_test.png", "PNG")

# make and store timestamped copy
ts = datetime.datetime.now().timestamp()
name = "history/perlin_{0}.png".format(ts)    
img.save(name, "PNG")

subprocess.run(["cp", "./perlin2.py", "./history/perlin_{0}.py".format(ts)])

#note: I'm on a mac and I usually run with: 
#python art.py; open -a Preview test.png
#which opens the image in preview as soon as it's done drawing
#not sure what the windows/linux equivalent is




