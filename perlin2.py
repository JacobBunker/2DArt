import numpy as np
from PIL import Image
import datetime;

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

desiredMax = 30.12 #30.12
interval = desiredMax / picSizeX
print(interval)
    
#make array 
temp = np.empty([picSizeX,picSizeY,3])
i = 0
while(i < picSizeX):
    ii = 0
    while(ii < picSizeY):
        tr = np.random.random()*0.1
        pout = perlin(i*tr*interval,ii*tr*interval)
        pout = (pout*10 + 255/2)
        if(pout < 0):
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


# convert array to Image
img = Image.fromarray(temp.astype('uint8'))
img.save("perlin_test.png", "PNG")

# make and store timestamped copy
ts = datetime.datetime.now().timestamp()
name = "history/perlin_{0}.png".format(ts)    
img.save(name, "PNG")


#note: I'm on a mac and I usually run with: 
#python art.py; open -a Preview test.png
#which opens the image in preview as soon as it's done drawing
#not sure what the windows/linux equivalent is




