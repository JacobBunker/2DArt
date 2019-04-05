import numpy as np
from PIL import Image
import datetime;

res = 2
    
def xfun(x,y,t):
    return x+(res*5)*np.cos(t*120)+(res*50)*np.cos(t*2)+(res*400)*np.cos(t/50)
    
def yfun(x,y,t):
    return y+(res*1)*np.sin(t*120)+(res*50)*np.sin(t*2)+(res*400)*np.sin(t/50)

sizeX = int(1000*res)
sizeY = int(1400*res)

#init array to black 
temp = np.empty([sizeX,sizeY,3])
i = 0
while(i < sizeX):
    ii = 0
    while(ii < sizeY):
        temp[i,ii,0] = 0#np.random.randint(0,255,dtype='uint8')
        temp[i,ii,1] = 0#np.random.randint(0,255,dtype='uint8')
        temp[i,ii,2] = 0#np.random.randint(0,255,dtype='uint8')
        ii += 1
    i += 1

print(temp.shape)


if(False):
    #center the starting point
    x = sizeX/2
    y = sizeY/2 - ((50*9)/2)

    #draw
    t = 0
    tMax = 400
    stepSize = 0.5
    while(t < tMax):
        i = 0
        while(i < 500):
            xt = xfun(x+(i*np.random.random()*5),y,t)
            yt = yfun(x+(i*np.random.random()*5),y+(np.random.random()*5),t)
            if(xt < sizeX and xt >= 0 and yt < sizeY and yt >= 0):
                ixt = int(xt)
                iyt = int(yt)
                temp[ixt,iyt,0] = 55#(t / tMax)*255
                temp[ixt,iyt,1] = ((tMax-t) / tMax)*255
                temp[ixt,iyt,2] = (t / tMax)*255
            i += 1 
              
        print("t:{0}\n".format(t))
        t += np.random.random()*stepSize



def xfun2(x,y,t):
    return x+np.random.random()*10*(t*res)
    
def yfun2(x,y,t):
    return y+np.random.random()*10*(t*res)

def xfun3(x,y,t):
    return x+7*np.cos(t/4)
    
def yfun3(x,y,t):
    return y+7*np.sin(t/4)


#draw
x = 0
y = 0
t = 0
tMax = 800
stepSize = 1
while(t < tMax):
    i = 0
    while(i < 100):
        yt = xfun2(x+(i*5),y,t)
        xt = yfun2(x+(i*5),y,t)
        ii = 0
        while(ii < 24):
            ixt = xfun3(xt, yt, ii)
            iyt = yfun3(xt, yt, ii)
            if(ixt < sizeX and ixt >= 0 and iyt < sizeY and iyt >= 0):
                iixt = int(ixt)
                iiyt = int(iyt)
                temp[iixt,iiyt,0] = ((tMax-t) / tMax)*255
                temp[iixt,iiyt,1] = 0
                temp[iixt,iiyt,2] = 0
            ii+=1
        i += 1 
              
    print("t:{0}\n".format(t))
    t += np.random.random()*stepSize
    

# convert array to Image
img = Image.fromarray(temp.astype('uint8'))
img.save("test.png", "PNG")

# make and store timestamped copy
ts = datetime.datetime.now().timestamp()
name = "history/{0}.png".format(ts)    
img.save(name, "PNG")


#note: I'm on a mac and I usually run with: 
#python art.py; open -a Preview test.png
#which opens the image in preview as soon as it's done drawing
#not sure what the windows/linux equivalent is




