'''
 Copyright (c) 2012, Jeffrey Lipton (jeff@seraphrobotics.com
 All rights reserved.
'''


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_LayerViewerWidget import *

class SegmentVisualizer(QWidget,  Ui_LayerViewWidget):
    """
    stackFile Visualizer is a widget which will display the layers of a stackFile
    every material is assigned a color based on their order in the file
    to release keyboard press esc
    to toggle between showing thin lines and pathwidth lines hit W
    to show thin lines overlayed on path widths high S then W
    to zoom, scroll mouse wheel or hit page up to zoom in, page down to zoom out
    to change layers, hit up arrow to change layer + , down arrow to change layer -
    
    """
    changeLayer = pyqtSignal(int,int)
    
    def __init__(self):
        super(SegmentVisualizer, self).__init__()
        self.setupUi(self)
        self.showWidth=False
        self.clearBetweenLayers = True
        
        
        #Set up GUI

        self.layerView.setScene(QGraphicsScene(self.layerView))
        self.layerView.scale(10, 10)
#        self.layerView.setDragMode(QGraphicsView.RubberBandDrag)
        
        
        self.pen=QPen()
        self.pen.setStyle(Qt.SolidLine)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setJoinStyle(Qt.RoundJoin)
        self.pen.setColor(Qt.black)

        self.layerSlider.setSingleStep(1)
        self.layerSpin.setSingleStep(1)
        
        self.innerCheck.setChecked(True)
        self.outerCheck.setChecked(True)
        
        
        #################connections
        self.layerSpin.valueChanged.connect(self.requestLayerChange)
        self.layerSlider.valueChanged.connect(self.requestLayerChange)
        self.outerCheck.clicked.connect(self._on_outerCheck)
        self.innerCheck.clicked.connect(self._on_innerCheck)
        
        self.grabKeyboard()

    def requestLayerChange(self):
        type = 0
        if (self.outerCheck.isChecked() and self.innerCheck.isChecked()): 
            type = 0
        elif (self.outerCheck.isChecked() and not self.innerCheck.isChecked()): 
            type = 2
        elif (not self.outerCheck.isChecked() and self.innerCheck.isChecked()): 
            type = 1
        elif (not self.outerCheck.isChecked() and not self.innerCheck.isChecked()): 
            type = 0
            
        self.changeLayer.emit(self.layerSpin.value(),type)
        
    def _on_outerCheck(self):
        if (not self.outerCheck.isChecked() and not self.innerCheck.isChecked()): 
            self.innerCheck.setChecked(True)
        self.requestLayerChange()
    def _on_innerCheck(self):
        if (not self.outerCheck.isChecked() and not self.innerCheck.isChecked()): 
            self.outerCheck.setChecked(True)
        self.requestLayerChange()
        
        
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Home:
            self.layerSpin.setValue(0)
        elif event.key()==Qt.Key_Up:
            self.layerSpin.stepUp()
        elif event.key()==Qt.Key_Down:
            self.layerSpin.stepDown()
        elif event.key()==Qt.Key_W:
            self.toggleWidth()
        elif event.key()==Qt.Key_S:
            self.toggleClear()
        elif event.key()==Qt.Key_PageUp:
            self.zoomIn()
        elif event.key()==Qt.Key_PageDown:
            self.zoomOut()
        elif event.key()==Qt.Key_Escape:
            self.releaseKeyboard()

            
    def wheelEvent(self, event):
        factor = 1.41**(-event.delta()/240.0)
        self.layerView.scale(factor, factor)
            
        
    def toggleWidth(self):
        if self.showWidth: self.showWidth = False
        else: self.showWidth = True
        self.loadLayer(self.layerInt)
        
    def toggleClear(self):
        if self.clearBetweenLayers: self.clearBetweenLayers = False
        else: self.clearBetweenLayers = True


    def zoomIn(self):
        self.layerView.scale(1.1, 1.1)
        
    def zoomOut(self):
        self.layerView.scale(.9, .9)
        
    def setBounds(self, xmin,xmax,ymin,ymax):
        self.layerView.setSceneRect( QRectF(QPointF(maxX, maxY), QPointF(minX, minY))) 
    
    def setZs(self,zs):
        self.layerSpin.setRange(0, len(zs)-1)
        self.layerSlider.setRange(0, len(zs)-1)

    def setZ(self,z):
        self.zSpin.setValue(z)

    
    def loadLoops(self,loops):
        scene = self.layerView.scene()
        if self.clearBetweenLayers: scene.clear()
        else: self.toggleClear()
        
        color = QColor(Qt.black) #self.matColors[materialName]
        if self.showWidth:
            width = 5.0#self.materials[materialName].getPropertyValue("pathWidth")
            self.pen.setWidthF(float(width))
            color.setAlphaF(0.5)
        else: 
            self.pen.setWidthF(0)
            color.setAlphaF(1.0)
        self.pen.setColor(color)
        
        for line in loops:
            scene.addLine(line, self.pen)


                                                    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form=SegmentVisualizer()
    form.loadLoops([[
        QLineF(QPointF(0,0),QPointF(100,100))
    ]])
    form.loadLoops([[
        QLineF(QPointF(100,0),QPointF(0,100))
    ]])
    form.show()
    
    app.exec_()

    
