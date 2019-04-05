import numpy as np
from PIL import Image
import datetime;


res = 1
sizeX = int(100*res)
sizeY = int(140*res)

res = 10
picSizeX = int(100*res)
picSizeY = int(140*res)

diffX = sizeX / picSizeX
diffY = sizeY / picSizeY

grid = np.empty([sizeX+1,sizeY+1,4,2])

gradients = [[1,1], [1,0], [1,-1], [0,1], [0,0], [0,-1],
             [-1,1], [-1,0], [-1,-1]]

def generateGradientVector():
    v = np.empty([2])
    x = (np.random.random() * 2) - 1
    y = (np.random.random() * 2) - 1
    l = np.linalg.norm([x,y])
    v[0] = x/l
    v[1] = y/l
    return v

def pickVector():
    t = gradients[np.random.randint(low=0,high=len(gradients))]
    return np.asarray(t)
    
i = 0
while(i < sizeX):
    ii = 0
    while(ii < sizeY):
        iii = 0
        while(iii < 4):
            grid[i,ii,iii] = pickVector()
            iii += 1
        #print(grid[i,ii], np.linalg.norm(grid[i,ii]))
        #print(grid[i,ii,:])
        ii += 1
    print(i)
    i += 1
    
exit()

def lerp( a0, a1, w):
    return ((1.0 - w)*a0) + (w*a1)

def dotGridGradient(ix, iy, x, y):
    dx = x - ix
    dy = y - iy
    return (dx*grid[ix,iy,0] + dy*grid[ix,iy,1])

def perlin(x, y):
    x0 = int(x*diffX);
    x1 = x0 + 1
    y0 = int(y*diffY);
    y1 = y0 + 1
    #print("x: {0} / {1} y: {2} / {3}".format(x, diffX, y, diffY))
    #print("x0: {0} y0: {1}".format(x0, y0))
    
    sx = x - x0
    sy = y - y0
    
    n0 = dotGridGradient(x0, y0, x, y)
    n1 = dotGridGradient(x1, y0, x, y)
    ix0 = lerp(n0, n1, sx)
    
    n0 = dotGridGradient(x0, y1, x, y)
    n1 = dotGridGradient(x1, y1, x, y)
    ix1 = lerp(n0, n1, sx)
    
    return lerp(ix0, ix1, sy)
    





#make array 
temp = np.empty([picSizeX,picSizeY,3])
i = 0
while(i < picSizeX):
    ii = 0
    while(ii < picSizeY):
        p = perlin(i,ii)
        #print(p)
        temp[i,ii,0] = p
        temp[i,ii,1] = 0#np.random.randint(0,255,dtype='uint8')
        temp[i,ii,2] = 0#np.random.randint(0,255,dtype='uint8')
        ii += 1
    i += 1

print(temp.shape)

tmax = np.max(temp[:,:,0])
tmin = np.min(temp[:,:,0])
trange = tmax - tmin
temp[:,:,0] = ((temp[:,:,0] - tmin) / trange) #* 255

i = 0
while(i < picSizeX):
    ii = 0
    while(ii < picSizeY):
        if(temp[i,ii,0] > 0.5):
            temp[i,ii,0] = 255
            temp[i,ii,1] = 0
            temp[i,ii,2] = 0
        else:
            temp[i,ii,0] = 0
            temp[i,ii,1] = 0
            temp[i,ii,2] = 255
        ii += 1
    i += 1

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




