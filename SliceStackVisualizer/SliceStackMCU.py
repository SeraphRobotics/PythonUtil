from PyQt4.QtCore import *
from SliceStack import *
from SliceStackVisualizer import *
####################################################################################


class SliceStackMCU(QObject):
    def __init__(self, file=""):
        self.UI = SliceStackVisualizer()
        self.stack = SliceStack(file)
        
        self.UI.setZs(self.stack.getZs())
        
        self.setLayer(4)
        ##self.connect(self.UI, SIGNAL("changeLayer(int)"), self.setLayer)
        ##self.UI.changeLayer.connect(self.setLayer)
        ##self.UI.layerSpin.valueChanged.connect(self.updateLayer)
        self.connect(self.UI.layerSlider, SIGNAL("valueChanged(int)"), self.setLayer)
        self.UI.show()
    
    def setFile(self,file):
        self.stack = SliceStack(file)
    
    
    def updateLayer(self):
        i = self.UI.layerSpin.value()
        self.setLayer(i)
    
    @pyqtSlot(int)
    def setLayer(self,int):
        print "setLayer"
        zs= self.stack.getZs()
        z = zs[int]
        self.UI.loadLoops(self.stack.getLoops(z))
        self.UI.setZ(z)

        
if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    x = SliceStackMCU(sys.argv[1])
    app.exec_()