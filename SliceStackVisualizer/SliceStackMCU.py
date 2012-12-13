from PyQt4.QtCore import *
from SliceStack import *
from SliceStackVisualizer import *
####################################################################################


class SliceStackMCU(QObject):
    def __init__(self, file=""):
        super(SliceStackMCU, self).__init__()
        self.UI = SliceStackVisualizer()
        self.stack = SliceStack(file)
        
        self.UI.setZs(self.stack.getZs())
        
        self.setLayer(0)
        self.UI.changeLayer.connect(self.setLayer)
        self.UI.show()
    
    def setFile(self,file):
        self.stack = SliceStack(file)
    
    
    def updateLayer(self):
        i = self.UI.layerSpin.value()
        self.setLayer(i)
    
    @pyqtSlot(int)
    def setLayer(self,int):
        zs= self.stack.getZs()
        z = zs[int]
        self.UI.loadLoops(self.stack.getLoops(z))
        self.UI.setZ(z)

        
        
    
        
if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    x = SliceStackMCU(sys.argv[1])
    app.exec_()