'''
 Copyright (c) 2010, Jeffrey Lipton (jil26@cornell.edu)

 All rights reserved.
 '''

from xml.etree.ElementTree import ElementTree , Element
from math import sqrt,  pow

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



def getPrimePoint(xn, xnminus, d):
    if (xn == xnminus):return xn
    delta = xn-xnminus
    delta.__mul__(d/delta.magnitude())
    return  xn + delta
    
def getDoublePrimePoint(xn, xnplus, d):
    if (xn == xnplus):return xn
    delta = xnplus-xn
    delta.__mul__(d/delta.magnitude())
    return xn+delta
    
def pointToElement(point_to_change):
    pointElement = Element("point")
    xEl = Element("x")
    yEl = Element("y")
    zEl = Element("z")
    xEl.text="%f"%point_to_change.getX()
    yEl.text="%f"%point_to_change.getY()
    zEl.text="%f"%point_to_change.getZ()
    pointElement.append(xEl)
    pointElement.append(yEl)
    pointElement.append(zEl)
    return pointElement
    
def elementToPoint(element):
    x = float(element.findall("x")[0].text)
    y = float(element.findall("y")[0].text)
    z = float(element.findall("z")[0].text)
    return Point(x, y, z)
    
    
def morphFabFile(fabfile,d,write_to_file = None):
    """
    http://www.xml.com/pub/a/2003/02/12/py-xml.html
    http://docs.python.org/library/xml.etree.elementtree.html
    """
    doc = ElementTree(file = fabfile )
        

    
    for element in doc.getiterator("path"): ## getiterator = iter in 2.7 on
        pointlist=[]
        primes=[]
        doubleprimes=[]
        finallist=[]
        elementpointlist = element.findall("point")

        
        # create points from elements        
        for el in elementpointlist: 
            pointlist.append(elementToPoint(el))
            element.remove(el)
        
        finallist.append(pointlist[0]) #add x0
        # create primes and double primes  and add x'n and x''n to finalist
        for i in range(1, len(pointlist)-1):
            xn = pointlist[i]
            xnplus = pointlist[i+1]
            xnminus = pointlist[i-1]
            p = getPrimePoint(xn, xnminus, d)
            dp=getDoublePrimePoint(xn, xnplus, d)
            finallist.append(p)
            finallist.append(dp)
        # add x'm
        xn = pointlist[-1]
        xnminus = pointlist[-2]
        pm = getPrimePoint(xn, xnminus, d)
        finallist.append(pm)
        
        
        for point in finallist: element.append(pointToElement(point))

    if write_to_file: doc.write(write_to_file)
    else: doc.write(file=fabfile,  encoding="UTF-8",  xml_declaration=True)
    
    return 1
    
if __name__ == "__main__":
    import sys
    if sys.argv[1]=="help":
        print "\n vinylFab.py 'fabfile' ('write name')"
    else:fabfile = sys.argv[1]
    
    
    if 2<len(sys.argv):  write_to_file = sys.argv[2]
    else: write_to_file = fabfile
    print morphFabFile(fabfile,1.0,  write_to_file)
    
