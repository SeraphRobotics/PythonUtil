from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree
from math import cos, sin, pi

from manipulations import *



DEG = 90.0 
AXIS = 'y'

CSPEED=30
CAMOUNT=10

YThreshold = 0.3
ZThreshold = 0.1
vThresh1 = 100
vThresh2 = 4
DThreshold = 0.5
HorizThreshold = .02



def slopeZY(point1, point2):
    p1list = pointListFromPointEl(point1)
    p2list = pointListFromPointEl(point2)
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
            if(DEBUG):print "empty path "
            continue
        #find minimum Z by searching all points
        minz =0
        for pointEl in pointEls:
            z = float(pointEl.find("z").text)
            if (z < minz): minz = z
        
        bottomlist= []
        
        for pointEl in PathEl.iter("point"):
            z = pointListFromPointEl(pointEl)[2]
            if ((minz+ZThreshold)>z): bottomlist.append(pointEl)
    
        if(DEBUG):print "#Points: ",len(pointEls), "  Bottom list len:", len(bottomlist)
        for pointEl in bottomlist:
            PathEl.remove(pointEl)
    
    return fabTree
    
def removeDeadPaths(fabTree):
    cmds = fabTree.getroot().find("commands")
    paths = cmds.findall("path")
    i=0
    for pathel in paths:
        if (len(pathel.findall("point"))<2):
            cmds.remove(pathel)
            if(DEBUG):print "path ",i,"is dead"
        i+=1
    return fabTree
    
def removeSides(fabTree):
    for PathEl in fabTree.iter("path"):
        pointEls = PathEl.findall("point")
        
        minY=10000
        maxY=-10000
        ## find the extreme Ys
        for pointEl in pointEls:
            y = pointListFromPointEl(pointEl)[1]
            if(y>maxY):maxY = y
            if(y<minY):minY = y
        
        minYDropList = []
        maxYDropList = []
        for pointEl in pointEls:
            y = pointListFromPointEl(pointEl)[1]
            if (y < (minY+YThreshold)):
                minYDropList.append(pointEl)
            elif ( y>(maxY-YThreshold)):
                maxYDropList.append(pointEl)
        
        ## THIS COULD LEAD to a problem if there is a sharp spike at the end
        for pointlist in [minYDropList,maxYDropList]:
            if (len(pointlist)):
                maxZ = -10000
                zDict={}
                for pointEl in pointlist:
                    z = pointListFromPointEl(pointEl)[2]
                    zDict[z] = pointEl
                    if (z>maxZ): maxZ = z
                if zDict.has_key(maxZ): 
                    pointlist.remove(zDict[maxZ])
                    for pointEl in pointlist:
                        PathEl.remove(pointEl)
                else: 
                    if(DEBUG):
                        print "could not find point for maxZ: ",maxZ
                        print "in keys ", zDict.keys()
                        print "for list ",list 
    return fabTree
            
            
    
def orderPathsInY(fabTree):
    #axis=2
    #{y,point)
    sortDirection= False
    for pathEl in fabTree.iter("path"):
        sortDirection= not sortDirection
        if(DEBUG): print "Path:", sortDirection
        pointYdict={}
        for pointEl in pathEl.iter("point"):
            y = pointListFromPointEl(pointEl)[1]
            pointYdict[y]=pointEl
        for pointEl in pathEl.findall("point"):        
            pathEl.remove(pointEl)
        ys = pointYdict.keys()
        ys = sorted(ys, reverse=sortDirection)
        for i in range(0,len(ys)):
            y = ys[i]
            pointEl = pointYdict[y]
            pathEl.append(pointEl)
            if(DEBUG): print "\ty: ", pointListFromPointEl(pointEl)[1]
    return fabTree
    
if __name__ == '__main__':
    import sys
    fabTree = ElementTree(file = sys.argv[1])
    fabTree = dropClearance(fabTree)
    fabTree = rotate(fabTree,float(DEG),AXIS)
    #writeTree("ROTATED.xdfl",fabTree)
    fabTree = removeBottom(fabTree)
    fabTree = removeDeadPaths(fabTree)
    #writeTree("NOBOTTOM.xdfl",fabTree)
    fabTree = removeSides(fabTree)
    #writeTree("NOSIDES.xdfl",fabTree)
    fabTree = orderPathsInY(fabTree)
    #writeTree("ORDERED.xdfl",fabTree)
    fabTree = removeDeadPaths(fabTree)
    #writeTree("CLEANED.xdfl",fabTree)
    fabTree = setClearance(fabTree,CAMOUNT,CSPEED)
    writeTree(sys.argv[2],fabTree)
