from PyQt4.QtCore import *
from XDFLFile import *
from XDFLView import *
####################################################################################


class XDFLMCU(QObject):
    def __init__(self, file=""):
        super(XDFLMCU, self).__init__()
        self.UI = XDFLView()
        self.stack = XDFLFile(file)
        
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
        self.UI.loadLines(self.stack.getLines(z))
        self.UI.setZ(z)

        
        
    
        
if __name__ == "__main__":
    import sys
    app  = QApplication(sys.argv)
    x = XDFLMCU(sys.argv[1])
    app.exec_()