'''
 Copyright (c) 2010, Jeffrey Lipton (jil26@cornell.edu)
 All rights reserved.
 '''

from xml.etree.ElementTree import ElementTree , Element
from math import sqrt,  pow


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            

class Point:
    ''' '''
    def __init__(self, x=0, y=0, z=0,  parent=None):
        self.x=x
        self.y=y
        self.z=z
        
    def magnitude(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    
    def setX(self, value):
        self.x=value
        
    def setY(self, value):
        self.y=value
        
    def setZ(self, value):
        self.z=value
        
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def getZ(self):
        return self.z
        
    def printpoint(self):
        print (self.x, self.y, self.z)
    
    def __add__(self, point):
        x = self.x + point.getX()
        y = self.y + point.getY()
        z = self.z + point.getZ()
        return Point(x, y, z)
    
    def __sub__(self, point):
        x = self.x - point.getX()
        y = self.y - point.getY()
        z = self.z - point.getZ()
        return Point(x, y, z)   
    
    def __mul__(self, value):
        self.x = self.x*value
        self.y = self.y*value
        self.z = self.z*value
        
    def __div__(self, value):
        self.x = self.x/value
        self.y = self.y/value
        self.z = self.z/value
    
    def __eq__(self, point):
        return ((self.x-point.getX())==(self.y-point.getY())==(self.z-point.getZ()))

    def toElement(self):
        pointElement = Element("point")
        xEl = Element("x")
        yEl = Element("y")
        zEl = Element("z")
        xEl.text="%f"%self.getX()
        yEl.text="%f"%self.getY()
        zEl.text="%f"%self.getZ()
        pointElement.append(xEl)
        pointElement.append(yEl)
        pointElement.append(zEl)
        return pointElement
    
def elementToPoint(element):
    x = float(element.findall("x")[0].text)
    y = float(element.findall("y")[0].text)
    z = float(element.findall("z")[0].text)
    return Point(x, y, z)
    
    
def MakeClearance(p1, p2, clearing, speed):
    p1prime = Point()
    p1prime.x = p1.x
    p1prime.y = p1.y
    p1prime.z = p1.z+clearing
    
    p2prime = Point()
    p2prime.x = p2.x
    p2prime.y = p2.y
    p2prime.z = p2.z+clearing
    
    pathel = Element("path")
    speedel = Element("speed")
    speedel.text="%f"%speed
    pathel.append(speedel)
    
    pathel.append(p1.toElement())
    pathel.append(p1prime.toElement())
    pathel.append(p2prime.toElement())
    pathel.append(p2.toElement())
    
    return pathel
    
    
    
    
    
    
    
    
def fab2XDFL(fabfile,write_to_file = None):
    """
    http://www.xml.com/pub/a/2003/02/12/py-xml.html
    http://docs.python.org/library/xml.etree.elementtree.html
    """
    fabtree = ElementTree(file = fabfile )
    fabroot = fabtree.getroot()
    
    xdflroot = Element("xdfl")
    xdfltree = ElementTree(xdflroot)
    
    clearance =0;
    id = 0;
    nameiddict={}
    #make Pallete
    pallete = Element("pallet");
    for matcalel in fabroot.getiterator("materialCalibration"):
        #get old info
        clearance = float(matcalel.findall("clearance")[0].text)
        name = matcalel.findall("name")[0].text
        id+=1
        nameiddict[name]= id
        ps = float(matcalel.findall("pathSpeed")[0].text)
        pw = float(matcalel.findall("pathWidth")[0].text)
        ph = float(matcalel.findall("pathHeight")[0].text)
        sb = float(matcalel.findall("suckback")[0].text)
        ac = float(matcalel.findall("depositionRate")[0].text)
        if (ac): ac = 1
        cv = 389.19*sb
        
        
        #make new tag
        xdflmat = Element("material")
        n = Element("name")
        idtag = Element("id")
        pwtag = Element("PathWidth")
        phtag = Element("PathHeight")
        pstag = Element("PathSpeed")
        actag = Element("AreaConstant")
        cvtag = Element("CompressionVolume")
        
        n.text = name
        idtag.text="%i"%id
        pwtag.text="%f"%pw
        phtag.text="%f"%ph
        pstag.text="%f"%ps
        actag.text="%f"%ac
        cvtag.text="%f"%cv
        
        xdflmat.append(n)
        xdflmat.append(idtag)
        xdflmat.append(pwtag)
        xdflmat.append(phtag)
        xdflmat.append(pstag)
        xdflmat.append(actag)
        xdflmat.append(cvtag)
        
        pallete.append(xdflmat)
        xdflroot.append(pallete)
    
    
    xdflcmds = Element("commands")
    # GO THROUGH PATHS
    
    lastpoint = Point(0, 0, 0)
    
    
    for element in fabroot.getiterator("path"): ## getiterator = iter in 2.7 on
        elementpointlist = element.findall("point")
        
        startpoint = elementToPoint(elementpointlist[0])
        btwpath = MakeClearance(lastpoint, startpoint, 10, 30)
        
        lastpoint = elementToPoint(elementpointlist[-1])
        
        xdflcmds.append(btwpath)
        
        #change name to id
        matcalnameel = element.findall("materialCalibrationName")[0]
        pathid = nameiddict[matcalnameel.text]
        element.remove(matcalnameel)
        idel = Element("materialID")
        idel.text = "%i"%pathid
        element.insert(0, idel)
        
        xdflcmds.append(element)
        
#        elementpointlist = element.findall("point")
#        # create points from elements        
#        for el in elementpointlist: 
#            pointlist.append(elementToPoint(el))
#            element.remove(el)
    
    xdflroot.append(xdflcmds)
    
    indent(xdflroot)
    xdfltree.write(file=write_to_file,  encoding="UTF-8")
    
    return 1
    
if __name__ == "__main__":
    import sys
    if sys.argv[1]=="help":
        print "\n fab2XDFL.py 'fabfile' ('xdfl name')"
    else:fabfile = sys.argv[1]
    
    
    if 2<len(sys.argv):  write_to_file = sys.argv[2]
    else: write_to_file = "result.xdfl"
    print fab2XDFL(fabfile,  write_to_file)
    
