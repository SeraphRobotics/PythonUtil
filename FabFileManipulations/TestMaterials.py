from xml.etree.ElementTree import ElementTree,  Element
from math import floor, sqrt,  pow

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
        

class PyMaterial():
    def __init__(self, namestring, pw, ph, ps, posb,  dr=0.00085, cl=10):
        self.name = namestring
        self.dict = {}
        self.dict["clearance"] = cl
        self.dict["depositionRate"] =dr
        self.name = namestring
        self.dict["pathSpeed"] = ps
        self.dict["pathWidth"] = pw
        self.dict["pausePath"] = 300
        self.dict["pitch"] = 0.000397
        self.dict["pushout"] = posb
        self.dict["suckback"] = posb
        self.dict["suckbackDelay"] = 0

    def toElement(self):
        matcal = Element("materialCalibration")
        el = Element("name")
        el.text = self.name
        matcal.append(el)
        
        for key in self.dict.keys():
            el = Element(key)
            el.text = "%f" %self.dict[key]
            matcal.append(el)
        return matcal
        
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

if __name__ == '__main__':
    import sys
    fabTree = ElementTree(Element("fabAtHomePrinter"))
    fabTree
    pw = 0.8
    ph = 0.8
    ps = 30
    posb  = 0.6
    mutli = 10
    lend=60
    matname="testingfrosting"
    
    root = fabTree.getroot()

    mat = PyMaterial(matname, pw, ph, ps, posb)
    root.append(mat.toElement())
    
    for i in range(0, mutli):
        path = PyPath(matname)
        path.addpointbycomp(i*pw, 0, ph)
        path.addpointbycomp(i, lend, ph)
        root.append(path.toElement())
    
    indent(fabTree.getroot())
    fabTree.write("test.fab")
    
