from FabFileLoader import *
from math import *
###################
from PyQt4.QtCore import *
from PyQt4.QtGui import *
###################


ZThreshold = 0.1
vThresh1 = 100
vThresh2 = 4
DThreshold = 0.5
HorizThreshold = .02


def slopeZY(point1, point2):
    dy = point1.y() - point2.y()
    dz = point1.z() - point2.z()
    s = 0
    if (0==dy): s=100000
    else: s = dz/dy
    return s


def findBottom(Path):
    ''' returns a list of the i values which form the bottom of the path
    '''
    points = Path.getPoints()
    
    #find minimum Z by searching all points
    minz =0
    for point in points:
        if (point.z() < minz): minz = point.z()
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
        if (s<HorizThreshold) and (point.z()<(minz+ZThreshold)):
            bottomlist.append(i)
        previouspoint = point
    return bottomlist
    


def graphPoints(scene, color,  points, ids, direction, idDirection=1):
        pen=QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setColor(color)
        pen.setWidthF(2.0)
        

        #Mark the bottom line segments
        i=0
        while(i<len(ids)):
            id = ids[i]
            if(id==0): previouspoint =points[id]
            else: previouspoint =points[id-1*idDirection]
            point = points[id]
            scene.addLine(QLineF(previouspoint.qtCoordinates(direction), point.qtCoordinates(direction)), pen)
            i=i+1



def bottomCheck(path,scene, direction=2):      
        bottomIDs = findBottom(path)
        points = path.getPoints()
        color = QColor(Qt.yellow)
        color.setAlphaF(.5)
        #Mark the bottom line segments
        graphPoints(scene, color, points, bottomIDs, direction)
            
        #expandBottomList
        fullBottomIDList=[]
        for id in bottomIDs:
            if(id!=0): fullBottomIDList.append(id-1)
            fullBottomIDList.append(id)
            
            
        #findExtreme Ys
        maxy = -10000
        maxyID = -1
        minyID =-1
        miny = 10000    
        for i in fullBottomIDList:
            y = points[i].y()
            if (y < miny): 
                miny=y
                minyID = i
            if (y>maxy):
                maxy = y
                maxyID= i
        print "Max Y:%f, id:%i\nMinY:%f, id:%i"%(maxy, maxyID, miny, minyID)
        
        extremum = [[maxyID, maxy], [minyID, miny]]
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
            
            color = QColor(Qt.green)
            color.setAlphaF(0.5)
            graphPoints(scene, color, points,extremumSideIDs, direction,  idDirection)
