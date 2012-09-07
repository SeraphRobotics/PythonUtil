from xml.etree.ElementTree import ElementTree 
import math

ZThreshold = 0.1
vThresh1 = 100
vThresh2 = 4
DThreshold = 0.5
HorizThreshold = .02

axes=["x","y","z"]


def elementToList(point)
    list = []
    for axis in axes:
        list.append(float(point.find[axis].text))
    return list

def slopeZY(point1, point2):

    p1 = elementToList(point1)
    p2 = elementToList(point2)

    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    s = 0
    if (0==dy): s=100000
    else: s = dz/dy
    return s


def findBottom(points):
    ''' returns a list of the i values which form the bottom of the path
    '''
   
    #find minimum Z by searching all points
    minz =0
    for point in points:
        z = float(point.find("z").text)
        if ( z < minz): minz = z
    print "min Z is ",  minz
    
    
    bottomlist = []
    #Case for i=0
    if ((minz+ZThreshold)>points[0]):bottomlist.append(0)

    #i>0
    for i in range(1, len(points)):
        point = points[i]
        previouspoint = points[i-1]
        s = abs(slopeZY(point, previouspoint))
        print "slope:", s
        if (s<HorizThreshold) and (point[2]<(minz+ZThreshold)):
            bottomlist.append(i)
        previouspoint = point
    return bottomlist
 
 
def trimSidesAndBottom(fabTree):
    for path in fabTree.getiterator("path"):
        points = path.findAll("point")
        bottomIDs = findBottom(points)
        #expandBottomList
        fullBottomIDList=[]
        for id in bottomIDs:
            if(id!=0): fullBottomIDList.append(id-1)
            fullBottomIDList.append(id)
        sideIDs = trimSides(points,fullBottomIDList)
        for id in fullBottomIDList:
            path.remove(points[id])
        for id in sideIDs:
            path.remove(points[id])
    
    
    

def  trimSides(points,fullBottomIDList):
    #findExtreme Ys
    maxy = -10000
    maxyID = -1
    minyID =-1
    miny = 10000    
    for i in fullBottomIDList:
        y = elementToList(points[i])[1]
        if (y < miny): 
            miny=y
            minyID = i
        if (y>maxy):
            maxy = y
            maxyID= i
    print "Max Y:%f, id:%i\nMinY:%f, id:%i"%(maxy, maxyID, miny, minyID)
    
    extremum = [[maxyID, maxy], [minyID, miny]]
    sideIDs = []
    for extreme in extremum:
        id = extreme[0]
        exy = extreme[1]
        
        extremumSideIDs=[]
        idDirection=-1
        if (fullBottomIDList.count(id-1)):idDirection=1
        
        counter = 0
        countThreshold=100000
        i = id
        metVThres1=0
        metVThres2=0
        bottompoint = points[id]
        while (counter<countThreshold):
            counter = counter+1
            print i, len(points)
            if (i>=len(points)-1) and (idDirection>0):
                ## reset id to loop around
                i = 0
                
            currentpoint = points[i+idDirection]
            lastpoint = points[i]
            i=i+idDirection
            
            slopeToBottom = abs(slopeZY(bottompoint, currentpoint))
            slopeBetweenPoints = abs(slopeZY(currentpoint, lastpoint))
            
            if not metVThres1:
                extremumSideIDs.append(i)
                if(slopeToBottom>vThresh1):
                    metVThres1 = 1
            elif not metVThres2:
                if(slopeBetweenPoints>vThresh2):
                    extremumSideIDs.append(i)
                else:
                    metVThres2 = 1
                    print "Slope between points ", slopeBetweenPoints
                    break
        extremumSideIDs.pop()
        sideIDs.extend(extremumSideIDs)
    return sideIDs