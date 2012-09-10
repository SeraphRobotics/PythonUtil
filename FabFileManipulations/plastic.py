'''
 Copyright (c) 2011, Jeffrey Lipton (jil26@cornell.edu)
 '''
from xml.etree.ElementTree import ElementTree,  Element
from math import floor

class PyPath():
    def __init__(self, matName):
        self.name = matName
        self.points =[]
    def addpoint(self, array):
        if (len(array)!=3): return
        self.points.append(array)
    def addpointbycomp(self, x, y, z):
        self.points.append([x, y, z])
    def addpoints(self, array):
        for point in array:
            self.addpoint(point)
    
    def toElement(self):
        path = Element("path")
        matcal = Element("materialCalibrationName")
        matcal.text=self.name
        path.append(matcal)
        for point in self.points:
            p = Element("point")
            x = Element("x")
            y = Element("y")
            z = Element("z")
            x.text = "%f"%point[0]
            y.text = "%f"%point[1]
            z.text = "%f"%point[2]
            p.append(x)
            p.append(y)
            p.append(z)
            path.append(p)
        return path


def raft(fabTree):
    root = fabTree.getroot()
    maxX=0
    maxY=0
    minX=300
    minY=300
    axes = ["x", "y", "z"]
    for path in fabTree.getiterator("path"):
        for point in path.findall("point"):
            for i in range(0, 3):
                el = point.find(axes[i])
                val = float(el.text)
                if(i==1 and val>maxY):maxY=val
                if(i==1 and val<minY):minY=val
                if(i==0 and val>maxX):maxX=val
                if(i==0 and val<minX):minX=val
    if (minX>maxX or minY>maxY):return fabTree
    
    pathWidth = 1.1;
    pathHeight = 0.465;
    density = 1.0/6.0
    
    ##give a little wiggle room:
    maxX+=2
    minX-=2
    maxY+=2
    minY-=2
    
    ## Make the Outer walls of the print raft
    wall1 = PyPath("plastic")
    
    wall1.addpoints([[minX, minY, -2*pathHeight], 
           [minX, maxY, -2*pathHeight],
           [maxX, maxY, -2*pathHeight],
           [maxX, minY, -2*pathHeight],
           [minX, minY, -2*pathHeight],
          ])
    
    wall2 = PyPath("plastic")
    
    wall2.addpoints([[minX, minY, -pathHeight], 
           [minX, maxY, -pathHeight],
           [maxX, maxY, -pathHeight],
           [maxX, minY, -pathHeight],
           [minX, minY, -pathHeight],
          ])
          
          
          

    ## Make Inner paths for layer 1
    numX = int(floor((maxY-minY)*density/pathWidth))
    x1 = minX+pathWidth
    x2 = maxX-pathWidth
    
    inner_paths1=[]
    for i in range(0, numX):
        inner = PyPath("plastic")

        y = minY+(1+i)*pathWidth/density
        inner.addpointbycomp(x1, y, -2*pathHeight)
        inner.addpointbycomp(x2, y, -2*pathHeight)
        inner_paths1.append(inner)
    
    
    ## Make Inner paths for layer 2
    numY = int(floor((maxX-minX)*density/pathWidth))
    y1 = minY+pathWidth
    y2 = maxY-pathWidth
    
    inner_paths2=[]
    for i in range(0, numX):
        inner = PyPath("plastic")

        x = minX+(1+i)*pathWidth/density
        inner.addpointbycomp(x, y1, -pathHeight)
        inner.addpointbycomp(x, y2, -pathHeight)
        inner_paths1.append(inner)
    
    
    root.insert(2, wall1.toElement())
    for i in range(0, len(inner_paths1)):
        root.insert(3+i, inner_paths1[i].toElement())
    root.insert(2+len(inner_paths1), wall2.toElement())
    for i in range(0, len(inner_paths2)):
        root.insert(4+len(inner_paths1), inner_paths2[i].toElement())
    
    
    
    
    
    return fabTree
    
    
       
    

 
 
if __name__ == '__main__':
    import sys
    fabTree = ElementTree(file = sys.argv[1])
    if len(sys.argv)>2: file = sys.argv[2]
    fabTree = raft(fabTree)
    fabTree.write(file)
    
    

