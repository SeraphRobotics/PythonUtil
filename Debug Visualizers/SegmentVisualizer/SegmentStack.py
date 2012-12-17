########################Imports####################################################
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree

from PyQt4.QtCore import *
####################################################################################


class SegmentStack():
    def __init__(self, file=""):
        self.zSliceDict={}
        self.setFile(file)

    
    def setFile(self,filestr):
        self.stackTree = ElementTree(file = filestr)
        for el in self.stackTree.iter(): el.tag = el.tag.lower()
        
        for slice in self.stackTree.getroot().iter("layer"):
            segment = slice.find("segment")
            point = segment.find("point")
            zel = point.find("z")
            z = float(zel.text)
            self.zSliceDict[z] = slice
    
    def getZs(self):
        return sorted(self.zSliceDict.keys())
    
    def getSegments(self,z):
        segments = []
        if not (self.zSliceDict.has_key(z)):return segments
        slice = self.zSliceDict[z]
        for segmentEl in slice.iter("segment"):
            segments.append(self.segment2Line(segmentEl))
        return segments
        
                        
    def segment2Line(self,segmentEl):
        '''converts a segment into a QLineF instance'''
        pointEls = segmentEl.findall("point")
        
        return QLineF(self.qPointFFromEl(pointEls[0]),self.qPointFFromEl(pointEls[1]))

    def qPointFFromEl(self, pointEl):
        x = float(pointEl.find("x").text)
        y = float(pointEl.find("y").text)    
        return QPointF(y,x) ## FOR coordinate transformation RHS to LHS

    
if __name__ == "__main__":
    import sys
    x= SliceStack(sys.argv[1])
    zs = x.getZs()
    print "zs: ",zs
    print x.getLoops(zs[0],2)


    