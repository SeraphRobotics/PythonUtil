from xml.etree.ElementTree import ElementTree,  Element
import math

ZThreshold = 0.1
vThresh1 = 100
vThresh2 = 4
DThreshold = 0.5
HorizThreshold = .04

axes=["x","y","z"]


def elementToList(point):
    list = []
    for axis in axes:
        list.append(float(point.find(axis).text))
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
    
    firstpoint = 0
    lastpoint = 0
    #Case for i=0
    
    if ((minz+ZThreshold)>elementToList(points[0])[2]): firstpoint = 1
    if ((minz+ZThreshold)>elementToList(points[-1])[2]): lastpoint = 1
#        bottomlist.append(0)
    

    #i>0
    for i in range(1, len(points)):
        point = elementToList(points[i])
        s = abs(slopeZY(points[i], points[i-1]))
        #print "slope:", s
        if (s<HorizThreshold) and (point[2]<(minz+ZThreshold)): # 
            bottomlist.append(i)
    return bottomlist,  firstpoint,  lastpoint
 
 
def trimSidesAndBottom(fabTree):
    firstpoint = 0
    lastpoint = 0
    sortDirection=1
    paths = fabTree.findall("path")
#    for path in fabTree.getiterator("path"):
#    for i in range(21,22):
    for i in range(0,len(paths)):
        path = paths[i]
        points = path.findall("point")
        print "number of points:",  len(points)
        bottomIDs,  firstpoint,  lastpoint = findBottom(points)
        if (len(bottomIDs)==0):
            print "Couldnt find bottom on path",  path
            pass
#        print "Bottom Points",  bottomIDs

        #expandBottomList
        fullBottomIDList=[]
        for id in bottomIDs:
            if(id!=0): fullBottomIDList.append(id-1)
            fullBottomIDList.append(id)


        # finds the sides based on the bottom
        sideIDs,  toDrop = trimSides(points,fullBottomIDList)
        
        toBeRemoved = fullBottomIDList + sideIDs
        if firstpoint: toBeRemoved.append(0)
        if lastpoint: toBeRemoved.append(len(points)-1)
        
        for j in range(0, len(toBeRemoved)):
            if (toBeRemoved[j]<0): toBeRemoved[j]= len(points)+toBeRemoved[j]
        toBeRemoved = sorted(list(set(toBeRemoved)))
        
        for id in toDrop:
            if (toBeRemoved.count(id)): toBeRemoved.remove(id)
        
        
        
        print "Path %i, to be removed is "%i ,  toBeRemoved
        
        for id in toBeRemoved:
            path.remove(points[id])
        
        orderPath(path, sortDirection)
        sortDirection= not sortDirection
        
    return fabTree
    
def orderPath(path, direction):#axis=2
    #{y,point)
    pointYdict={}
    for point in path.getiterator("point"):
        y = elementToList(point)[1]
        pointYdict[y]=point
        path.remove(point)
    ys = pointYdict.keys()
    if (direction>0):#asscending
        ys = sorted(ys)
    else: #decending
        ys = sorted(ys, reverse=True)
    for y in ys:
        point = pointYdict[y]
        path.append(point)
    


def  trimSides(points,fullBottomIDList):
    numpoints = len(points)
    
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
#    print "**** Max Y:%f, id:%i****\n****MinY:%f, id:%i ****"%(maxy, maxyID, miny, minyID)
    
    extremum = [[maxyID, maxy], [minyID, miny]]
    sideIDs = []
    toDrop=[]
    for extreme in extremum:
        id = extreme[0]
        exy = extreme[1]
        
        extremumSideIDs=[]
        idDirection=-1
        if (fullBottomIDList.count(id-1)):idDirection=1
        print "Extremum [max=0, min=1]:", extremum.index(extreme)
        print "\tFullButtom IDs",  fullBottomIDList
        print "\tDoes it contain:%i, -1"%id
        
        
        counter = 0
        i = id
        metVThres1=0
        metVThres2=0
        bottompoint = points[id]
        while ((counter<numpoints) and not metVThres2):
            counter = counter+1
            if (i>=len(points)-1) and (idDirection>0):
                ## reset id to loop around
                i = 0
                
            currentpoint = points[i+idDirection]
            lastpoint = points[i]
            i=i+idDirection
            
            slopeToBottom = abs(slopeZY(bottompoint, currentpoint))
            slopeBetweenPoints = abs(slopeZY(currentpoint, lastpoint))
#            print "%i"%i
#            print "\t Direction %i"%idDirection
#            print "\t slope to:",   slopeToBottom
#            print "\t slope between:",  slopeBetweenPoints
#            print "\t Current:",  elementToList(currentpoint)
#            print"\t LastPoint:",  elementToList(lastpoint)
#            print"\t BottomPoint",  elementToList(bottompoint)
            
            if not metVThres1:
                extremumSideIDs.append(i)
                if(slopeToBottom>vThresh1):
                    metVThres1 = 1
                    print "met thresh 1"
            elif not metVThres2:
                if(slopeBetweenPoints>vThresh2):
                    extremumSideIDs.append(i)
                else:
                    metVThres2 = 1
                    print "Met Thres 2, Slope between points ", slopeBetweenPoints
        ##extremumSideIDs.pop()
        sideIDs.extend(extremumSideIDs)
        toDrop.append(extremumSideIDs[-1])
        
    return sideIDs, toDrop
    
    

def solveHolesInLayers(fabTree, PathWidth, direction=2):
    """turns a list of paths into a list of of a list of paths with the same Z value"""
    slices={}
    root = fabTree.getroot()
    for path in fabTree.getiterator("path"):
        slicekey = 0 
        if (direction ==2): 
            slicekey = float(path.find("point").find("z").text)
        elif (direction ==1): 
            slicekey = float(path.find("point").find("y").text)
        elif (direction ==0): 
            slicekey = float(path.find("point").find("x").text)
            
        if slicekey in slices.keys(): slices[slicekey].append(path)
        else: slices[slicekey]=[path]
        root.remove(path)

    slicekeys =  sorted(slices.keys())
    for i in range(0, len(slicekeys)-1):
        current = slicekeys[i]
        next = slicekeys[i+1]
        delta = abs(next-current)
        for path in slices[current]:
            root.append(path)
        if (delta >2.0*PathWidth):
            numPaths = int(delta/PathWidth)-1
            for j in range(0, numPaths):
                toTranslate = (j+1)*PathWidth
                newPath = translatedPath(path, toTranslate, direction)
                root.append(newPath)
                print "ADDED NEW PATH"
    
    return fabTree

def translatedPath(path, toTranslate, direction = 2):
    axis = axes[direction]
    delta = [0, 0, 0]
    delta[direction] = toTranslate
    print "Delta ",  delta
    newpath = Element("path")
    matcalEl = path.find("materialCalibrationName")
    newpath.append(matcalEl)
    for point in path.getiterator("point"):
        p = Element("point")
        for axis in axes:
            value = float(point.find(axis).text)
            el = Element(axis)
            newval = value+delta[axes.index(axis)]
            el.text = "%f"%(newval)
            print "Shifted %s from %f to %f"%(axis, value, newval)
            p.append(el)
        newpath.append(p)
    
    return newpath
    





if __name__ == '__main__':
    import sys
    todo = sys.argv[1]
    
    if todo== "help":
        print "\northoticTrim.py 'file name old' 'file name 2' "
    elif len(sys.argv)< 2:
        print "need more arguments. type help"
    
    else: 
        fabTree = ElementTree(file = sys.argv[1])
        fabTree = trimSidesAndBottom(fabTree)
        print "starting"
        fabTree.write(sys.argv[2])
        print "done"
    
