########################Imports####################################################
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree

from PyQt4.QtCore import *
####################################################################################


class XDFLFile():
    def __init__(self, file=""):
        self.zSliceDict={}
        self.setFile(file)

    
    def setFile(self,filestr):
        self.stackTree = ElementTree(file = filestr)
        for el in self.stackTree.iter(): el.tag = el.tag.lower()
        
        cmds = self.stackTree.getroot().find("commands")
        for pathEl in cmds.iter("path"):
            matids = pathEl.findall("materialid")
            if (0!=len(matids)):
                pointEl = pathEl.find("point")
                zel = pointEl.find("z")
                z = float(zel.text)
                if self.zSliceDict.has_key(z):
                    self.zSliceDict[z].append(pathEl)
                else:
                    self.zSliceDict[z] = [pathEl]
                    
    
    def getZs(self):
        return sorted(self.zSliceDict.keys())
    
    def getLines(self,z):
        lines = []
        if not (self.zSliceDict.has_key(z)):return lines
        pathEls = self.zSliceDict[z]
        for pathEl in pathEls:
            for line in self.pathEl2Line(pathEl):
                lines.append(line)
        return lines
        
                        
    def pathEl2Line(self,pathEl):
        '''converts a segment into a QLineF instance'''
        lines=[]
        pointEls = pathEl.findall("point")
        
        for i in range(1,len(pointEls)):
            lines.append(QLineF(self.qPointFFromEl(pointEls[i-1]),self.qPointFFromEl(pointEls[i])))
        return lines
        

    def qPointFFromEl(self, pointEl):
        x = float(pointEl.find("x").text)
        y = float(pointEl.find("y").text)    
        return QPointF(y,x) ## FOR coordinate transformation RHS to LHS

    
if __name__ == "__main__":
    import sys
    x= XDFLFile(sys.argv[1])
    zs = x.getZs()
    print "zs: ",zs
    print x.getLayer(zs[0])


    