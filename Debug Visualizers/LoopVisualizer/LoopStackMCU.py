from PyQt4.QtCore import *
from LoopStack import *
from LoopStackVisualizer import *
####################################################################################


class LoopStackMCU(QObject):
    def __init__(self, file=""):
        super(LoopStackMCU, self).__init__()
        self.UI = LoopStackVisualizer()
        self.stack = LoopStack(file)
        
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
        self.UI.loadLoops(self.stack.getLoops(z))
        self.UI.setZ(z)

        
        
    
        
if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    x = LoopStackMCU(sys.argv[1])
    app.exec_()