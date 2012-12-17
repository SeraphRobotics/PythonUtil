from PyQt4.QtCore import *
from SegmentStack import *
from SegmentStackVisualizer import *
####################################################################################


class SegmentStackMCU(QObject):
    def __init__(self, file=""):
        super(SegmentStackMCU, self).__init__()
        self.UI = SegmentVisualizer()
        self.stack = SegmentStack(file)
        
        self.UI.setZs(self.stack.getZs())
        
        self.setLayer(0)
        self.UI.changeLayer.connect(self.setLayer)
        self.UI.show()
    
    def setFile(self,file):
        self.stack = SliceStack(file)
    
    
    def updateLayer(self):
        i = self.UI.layerSpin.value()
        self.setLayer(i)
    

    def setLayer(self,index,type=0):
        zs= self.stack.getZs()
        z = zs[index]
        self.UI.loadLoops(self.stack.getSegments(z))
        self.UI.setZ(z)

        
        
    
        
if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    x = SegmentStackMCU(sys.argv[1])
    app.exec_()