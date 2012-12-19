########################Imports####################################################
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree

from PyQt4.QtCore import *
####################################################################################


class LoopStack():
    def __init__(self, file=""):
        self.zSliceDict={}
        self.setFile(file)

    
    def setFile(self,filestr):
        self.stackTree = ElementTree(file = filestr)
        for el in self.stackTree.iter(): el.tag = el.tag.lower()
        
        for slice in self.stackTree.getroot().iter("layer"):
            segment = slice.find("loop")
            point = segment.find("point")
            zel = point.find("z")
            z = float(zel.text)
            self.zSliceDict[z] = slice
    
    def getZs(self):
        return sorted(self.zSliceDict.keys())
    
    def getLoops(self,z):
        ''' 1 = inner, 2 = outer , all others = all'''
        loops = []
        if not (self.zSliceDict.has_key(z)):return loops
        slice = self.zSliceDict[z]
        for loopEl in slice.iter("loop"):
            loops.append(self.loop2LineStack(loopEl))
        return loops
        
                        
    def loop2LineStack(self,loopEl):
        '''converts a loop into a list of QLineF instances'''
        lines =[]
        
        ## NEW VERSION THAT USES ETREE directly
        previouspoint = self.qPointFFromEl(loopEl.findall("point")[-1])
        for pointEl in loopEl.iter("point"):
            newpoint = self.qPointFFromEl(pointEl)
            lines.append(QLineF(previouspoint,newpoint ))
            previouspoint=newpoint 
        return lines
        
    def qPointFFromEl(self, pointEl):
        x = float(pointEl.find("x").text)
        y = float(pointEl.find("y").text)    
        return QPointF(y,x) ## FOR coordinate transformation RHS to LHS

    
if __name__ == "__main__":
    import sys
    x= LoopStack(sys.argv[1])
    zs = x.getZs()
    print "zs: ",zs
    print x.getLoops(zs[0],2)


    