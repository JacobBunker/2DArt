import numpy as np
from PIL import Image
import datetime;
import subprocess

picSizeX = 1000
picSizeY = 1400

#make array 
temp = np.empty([picSizeX,picSizeY,3])

start = np.asarray([picSizeX/2, picSizeY/2])

def getNext(p,d):
    return np.asarray([p[0] + np.random.random()*d, p[1] + np.random.random()*d])

pointCount = 0
points = np.empty([5,2])

points[0] = start
points[1] = getNext(points[0],100)
points[2] = getNext(points[1],100)

def draw(p,t):
    return ((((1-t)**2)*p[0]) + (2*t*(1-t)*p[1]) + ((t**2)*p[2]))
    
if(True):
    z = 0
    while(z < 1):
        t = 0
        tMax = 1.
        stepSize = 0.01
        while(t < tMax):
            newP = draw(points,t)
            if(newP[0] < picSizeX and newP[0] >= 0 and newP[1] < picSizeY and newP[1] >= 0):
                ixt = int(newP[0])
                iyt = int(newP[1])
                temp[ixt,iyt,0] = 0
                temp[ixt,iyt,1] = 0
                temp[ixt,iyt,2] = 255#(t / tMax)*255
            t += stepSize
        z += 1

name = "bezier_tree"

# convert array to Image
img = Image.fromarray(temp.astype('uint8'))
img.save("{0}_test.png".format(name), "PNG")

# make and store timestamped copy
ts = datetime.datetime.now().timestamp()
picName = "history/{0}_{1}.png".format(name,ts)    
img.save(picName, "PNG")

subprocess.run(["cp", "./{0}.py".format(name), "./history/{0}_{1}.py".format(name,ts)])

#note: I'm on a mac and I usually run with: 
#python art.py; open -a Preview test.png
#which opens the image in preview as soon as it's done drawing
#not sure what the windows/linux equivalent is




