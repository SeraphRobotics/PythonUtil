from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree
from math import cos, sin, pi

from manipulations import *

ZThreshold = 0.1
vThresh1 = 100
vThresh2 = 4
DThreshold = 0.5
HorizThreshold = .02


def listFromPointEl(pointEl):
    values=[0,0,0]
    values[0] = float(pointEl.find("x").text)
    values[1] = float(pointEl.find("y").text)
    values[2] = float(pointEl.find("z").text)
    return values

def slopeZY(point1, point2):
    p1list = listFromPointEl(point1)
    p2list = listFromPointEl(point2)
    dy = p1list[1] - p2list[1]
    dz = p1list[2] - p2list[2]
    s = 0
    if (0==dy): s=100000
    else: s = dz/dy
    return s

def removeBottom(fabTree):
    
    for PathEl in fabTree.iter("path"):
        pointEls = PathEl.findall("point")
        if not len(pointEls): 
            print "empty path "
            continue
        #find minimum Z by searching all points
        minz =0
        for pointEl in pointEls:
            z = float(pointEl.find("z").text)
            if (z < minz): minz = z
        
        bottomlist= []
        

        #Case for i=0
        point0z = float(pointEls[0].find("z").text)
        if ((minz+ZThreshold>point0z)):
            bottomlist.append(pointEls[0])
        
        #i>0
        for i in range(1, len(pointEls)):
            pointEl = pointEls[i]
            point_z = float(pointEls[i].find("z").text)
            previouspointEl = pointEls[i-1]
            s = abs(slopeZY(pointEl, previouspointEl))
            #print "slope on the bottom:", s
            #if (s<HorizThreshold) and (point_z<(minz+ZThreshold)):
            if (point_z<(minz+ZThreshold)):
                bottomlist.append(pointEls[i])
    
        for pointEl in bottomlist:
            PathEl.remove(pointEl)
    
    return fabTree
    
    
def orderPathsInY(fabTree):
    #axis=2
    #{y,point)
    sortDirection= False
    for pathEl in fabTree.iter("path"):
        sortDirection= not sortDirection
        print "Path:", sortDirection
        pointYdict={}
        for pointEl in pathEl.iter("point"):
            y = listFromPointEl(pointEl)[1]
            pointYdict[y]=pointEl
            pathEl.remove(pointEl)
        ys = pointYdict.keys()
        ys = sorted(ys, reverse=sortDirection)
        for y in ys:
            pointEl = pointYdict[y]
            pathEl.append(pointEl)
            print "\ty: ", listFromPointEl(pointEl)[1]
    return fabTree
    
if __name__ == '__main__':
    import sys
    fabTree = ElementTree(file = sys.argv[1])
    fabTree = dropClearance(fabTree)
    fabTree = removeBottom(fabTree)
    #fabTree = orderPathsInY(fabTree)
    fabTree.write(sys.argv[2])
