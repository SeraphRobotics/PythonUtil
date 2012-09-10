'''
 Copyright (c) 2011, Jeffrey Lipton (jeffreyilipton@gmail.com) all rights reserved
 '''
from xml.etree.ElementTree import ElementTree,  Element
from math import floor, sqrt,  pow


class FabPoint:
    ''' '''   
    def __init__(self, x=0, y=0, z=0,  parent=None):
        self.x=x
        self.y=y
        self.z=z

    def __init__(self, element):
        self.x=0
        self.y=0
        self.z=0
        for el in element.getiterator():
            if (str.lower(el.tag)=="x"):  self.x = float(el.text)
            elif (str.lower(el.tag)=="y"):  self.y = float(el.text)
            elif (str.lower(el.tag)=="z"):  self.z = float(el.text)
        
    def toElement(self):
        pointElement = Element("point")
        xEl = Element("x")
        yEl = Element("y")
        zEl = Element("z")
        xEl.text="%f"%self.x
        yEl.text="%f"%self.y
        zEl.text="%f"%self.z
        pointElement.append(xEl)
        pointElement.append(yEl)
        pointElement.append(zEl)
        return pointElement

    def magnitude(self):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    
    def __add__(self, point):
        x = self.x + point.x
        y = self.y + point.y
        z = self.z + point.z
        return Point(x, y, z)
    
    def __sub__(self, point):
        x = self.x - point.x
        y = self.y - point.y
        z = self.z - point.z
        return Point(x, y, z)   
    
    def __mul__(self, value):
        self.x = self.x*value
        self.y = self.y*value
        self.z = self.z*value
        
    def __div__(self, value):
        if (value==0): return 
        self.x = self.x/value
        self.y = self.y/value
        self.z = self.z/value
    
    def __eq__(self, point):
        return ((self.x-point.getX())==(self.y-point.getY())==(self.z-point.getZ()))


class FabPath:
    def __init__(self, matName):
        self.name = matName
        self.points =[]

    def __init__(self, element):
        self.name=""
        self.points=[]
        for el in element.getiterator():
            if (str.lower(el.tag)=="materialcalibrationname"): self.name = el.text
            elif(str.lower(el.tag)=="point"): self.points.append(FabPoint(el))

    
    def addpoint(self, point):
        self.points.append(point)
        
    def addpoints(self, array):
        for point in array:
            self.addpoint(point)
    
    def toElement(self):
        path = Element("path")
        matcal = Element("materialCalibrationName")
        matcal.text=self.name
        path.append(matcal)
        for point in self.points:
            path.append(point.toElement())
        return path

class FabMaterial:
    def __init__(self, name, pathwidth, pathspeed, clearance, dr, suckback, suckbackDelay,  pausePaths=300,  pitch=0.000397, pathheight=0.0 ):
        self.name = name
        self.pathwidth = pathwidth
        self.pathheight = pathheight
        self.pathspeed = pathspeed
        self.clearance = clearance
        self.depositionrate=dr
        self.suckback = suckback
        self.suckbackdelay = suckbackDelay
        self.pausepaths = pausePaths
        self.pitch = pitch
    
    def __init__(self, element):
        self.pathheight=0
        for el in element.getiterator():
            if (str.lower(el.tag)== "name"):  self.name = el.text
            elif(str.lower(el.tag)== "pathwidth"):  self.pathwidth = float(el.text)
            elif(str.lower(el.tag)== "pathheight" or str.lower(el.tag)== "sliceheight"):  self.pathheight = float(el.text)
            elif(str.lower(el.tag)== "pathspeed"):  self.pathspeed = float(el.text)
            elif(str.lower(el.tag)== "clearance"):  self.clearance = float(el.text)
            elif(str.lower(el.tag)== "depositionrate"):  self.depositionrate = float(el.text)
            elif(str.lower(el.tag)== "suckback"):  self.suckback = float(el.text)
            elif(str.lower(el.tag)== "suckbackdelay"):  self.suckbackdelay = float(el.text)
            elif(str.lower(el.tag)== "pausepaths"):  self.pausepaths = int(el.text)
            elif(str.lower(el.tag)== "pitch"):  self.pitch = float(el.text)
        
    def toElement(self):
        matEl = Element("materialCalibration")
        dict={"name":self.name,
             "pathWidth":"%f"%self.pathwidth, 
             "pathSpeed":"%f"%self.pathspeed, 
             "clearance":"%f"%self.clearance, 
             "depositionRate":"%f"%self.depositionrate, 
             "suckback": "%f"%self.suckback, 
             "pushout":"%f"%self.suckback, 
             "suckbackDelay": "%f"%self.suckbackdelay, 
             "pitch":"%f"%self.pitch, 
             "pausePaths":"%i"%self.pausepaths             
             }
             
        if self.pathheight: dict["pathHeight"] = "%f"%self.pathheight
        
        for tag in dict.keys():
            el = Element(tag)
            el.text = dict[tag]
            matEl.append(el)
        
        return matEl
        
        

class FabFile:
    def __init__(self, fabTree):
        self.materials=[]
        self.commands=[]
        
        
        root = fabTree.getroot()
        self.printaccel = float(fabTree.find("printAcceleration").text)
        
        for matEl in root.getiterator("materialCalibration"):
            self.materials.append(FabMaterial(matEl))
        
        for pathEl in root.getiterator("path"):
            self.commands.append(FabPath(pathEl))
        
    
    def toFabTree(self):
        root = Element("fabAtHomePrinter")
        printAccelEl = Element("printAcceleration")
        printAccelEl.text="%f"%self.printaccel
        root.append(printAccelEl)
        for mat in self.materials:
            root.append(mat.toElement())
        for command in self.commands:
            root.append(command.toElement())
            
        return ElementTree(root)
        
        


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

if __name__=="__main__":
    import sys
    infile = sys.argv[1]
    outfile = sys.argv[2]
    
    x = FabFile(ElementTree(file=infile))
    tree = x.toFabTree()

    indent(tree.getroot())
    tree.write(outfile)
