import numpy as np
from PIL import Image
import datetime;
import subprocess

picSizeX = 1000
picSizeY = 1400

#make array 
temp = np.empty([picSizeX,picSizeY,3])

def getNext(p,d,z):
    xSkew = np.sin(np.radians(z*10))
    ySkew = np.cos(np.radians(z*10))
    print("xsk: {0} ysk: {1}".format(xSkew, ySkew))
    return np.asarray([p[0] + (np.random.random() - 0.5 + xSkew)*d, p[1] + (np.random.random() - 0.5 + ySkew)*d])
    
def splitPoint(p1, p2):
    return np.asarray([(p1[0] + p2[0])/2, (p1[1] + p2[1])/2])


def getCurves(start, curves):
    zSkew = (np.random.random() -0.5 * 360)
    points = np.empty([1+(curves*3),2])
    d = 10
    points[0] = start
    i = 1
    print(points.shape)
    while(i < points.shape[0]):
        if(i == points.shape[0] - 1 or i%3 != 0):
            points[i] = getNext(points[i - 1],d,(i+zSkew))
            i += 1
        else: #at the fourth point
            points[i+1] = getNext(points[i - 1],d*2,(i+zSkew))
            points[i] = splitPoint(points[i-1],points[i+1])
            #do both the fourth and fifth point
            i += 2
    return points

def drawQuad(p,t):
    return ((((1-t)**2)*p[0]) + (2*t*(1-t)*p[1]) + ((t**2)*p[2]))
    
def drawCube(p,t):
    return ((((1-t)**3)*p[0]) + (3*t*((1-t)**2)*p[1]) + (3*(t**2)*(1-t)*p[2]) + ((t**3)*p[3]))
    
def drawCircle(x,y,radius):
    def xfun(x,y,t,radius):
        return x+(radius*np.cos(np.radians(t*3)))
    
    def yfun(x,y,t,radius):
        return y+(radius*np.sin(np.radians(t*3)))
    #print("\tcircle")
    t = 0
    tMax = 360/3
    stepSize = 1.
    while(t < tMax):
        xt = xfun(x,y,t,radius)
        yt = yfun(x,y,t,radius)
        if(xt < picSizeX and xt >= 0 and yt < picSizeY and yt >= 0):
            ixt = int(xt)
            iyt = int(yt)
            temp[ixt,iyt,0] = 255
            temp[ixt,iyt,1] = 0
            temp[ixt,iyt,2] = 0#(t / tMax)*255
        t += stepSize

def drawLines(start,curves,level):
    points = getCurves(start,curves)
    colorOffset = level*50
    if(colorOffset > 255):
        colorOffset = 255
    z = 0
    while(z < points.shape[0]-1):
        print("z at {0}".format(z))
        #print(points[z:z+4])
        if(level < 1):
            drawCircle(points[z,0],points[z,1],3)
            drawLines(points[z],int(curves/2),level+1)
        t = 0
        tMax = 1.
        stepSize = 0.01
        while(t < tMax):
            newP = drawCube(points[z:z+4],t)
            if(newP[0] < picSizeX and newP[0] >= 0 and newP[1] < picSizeY and newP[1] >= 0):
                ixt = int(newP[0])
                iyt = int(newP[1])
                temp[ixt,iyt,0] = colorOffset
                temp[ixt,iyt,1] = 0
                temp[ixt,iyt,2] = 255#(t / tMax)*255
            t += stepSize
        z += 3
        

start = np.asarray([picSizeX/2, picSizeY/2])        
drawLines(start,12,0)

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




