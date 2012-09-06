from FabFileLoader import *
from math import *
###################
from PyQt4.QtCore import *
from PyQt4.QtGui import *
###################


ZThreshold = 0.1
VertThreshold1 = 100
VertThreshold2 = 50
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
    '''Find the minimum Z value and all points with that value are the bottom.
     Also, Grow line segments together. Check if te next slope is aproimately the same as the last slope
    '''
    
    minz =0
    for point in Path.getPoints():
        if (point.z() < minz): minz = point.z()
    print "min Z is ",  minz
    
    
    bottomlist = []
    previouspoint = Path.getPoints()[0]
    for point in Path.getPoints()[1:]:
        s = abs(slopeZY(point, previouspoint))
        print "slope:", s
        delta = point-previouspoint
        if (s<HorizThreshold) and (DThreshold <delta.magnitude()) and (point.z()<(minz+ZThreshold)):
            bottomlist.append(point)
            bottomlist.append(previouspoint)
        previouspoint = point
    return bottomlist
    


def bottomCheck(path,scene, direction=2):
        pen=QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        color = QColor(Qt.yellow)
        color.setAlphaF(.5)
        pen.setColor(color)
        pen.setWidthF(2.0)
        
        bottompoints = findBottom(path)
        if len(bottompoints):
            i=1
            while(i<len(bottompoints)):
                previouspoint = bottompoints[i-1]
                point = bottompoints[i]
                scene.addLine(QLineF(previouspoint.qtCoordinates(direction), point.qtCoordinates(direction)), pen)
                i=i+2
        
        
    
