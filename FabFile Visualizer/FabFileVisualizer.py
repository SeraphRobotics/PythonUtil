'''
This file is part of the Fab@Home Project.
 Fab@Home operates under the BSD Open Source License.

 Copyright (c) 2010, Jeffrey Lipton (jil26@cornell.edu)

 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:
     * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
     * Neither the name of the <organization> nor the
       names of its contributors may be used to endorse or promote products
       derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNERS OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 '''


from FabFileLoader import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_LayerViewerWidget import *

class FabFileVisualizer(QWidget,  Ui_LayerViewWidget):
    """
    FabFile Visualizer is a widget which will display the layers of a fabfile
    every material is assigned a color based on their order in the file
    to release keyboard press esc
    to toggle between showing thin lines and pathwidth lines hit W
    to show thin lines overlayed on path widths high S then W
    to zoom, scroll mouse wheel or hit page up to zoom in, page down to zoom out
    to change layers, hit up arrow to change layer + , down arrow to change layer -
    
    """
    def __init__(self, fabFile=None):
        super(FabFileVisualizer, self).__init__()
        self.setupUi(self)
        self.fabFile=fabFile
        self.setLayers([])
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
        self.connect(self.layerSpin, SIGNAL("valueChanged(int)"), self.loadLayer)
        self.connect(self.layerSlider, SIGNAL("valueChanged(int)"), self.loadLayer)
        
        self.grabKeyboard()

        
        
        #Needs to be after Setting up GUI
        if self.fabFile: self.loadFabFile(fabFile)
        
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
        
    def loadFabFile(self, fabFile):
        self.fabFile=fabFile
        (materials, pathstack)=processFabFile(fabFile)
        self.setMaterials(materials)
        layers= sortPathsIntoLayers(pathstack)
        self.setLayers(layers)
        self.loadLayer(0)


    def setMaterials(self, materials, colors = None):
        '''assigns materials and optionally QColors'''
        self.materials=materials
        
        self.matColors={}
        if not colors:
            colors = [Qt.black, Qt.red, Qt.green, Qt.blue, Qt.magenta, Qt.darkYellow]
            colors = [QColor(color) for color in colors]

            
        if len(self.materials)>len(colors) :
            for i in range(0, len(self.materials)-len(colors)):
                color = colors[i]
                colors.append(color.lighter(175))
        
        for material in self.materials:
            self.matColors[material]=colors.pop(0)
    
    def getMaterials(self):
        """returns a list of strings containing the names of the materials"""
        return self.materials
             

    def loadLayer(self, layerInt):
        '''changes to the ith layer of the fab file'''
        scene = self.layerView.scene()
        if self.clearBetweenLayers: scene.clear()
        else: self.toggleClear()
        
        if (layerInt < len(self.layers)):
            self.layerInt=layerInt
            for path in self.layers[layerInt]:
            
                materialName = path.getMaterial()
                print materialName
                print self.matColors
                color = QColor(Qt.black) #self.matColors[materialName]
    
                if self.showWidth:
                    width = self.materials[materialName].getPropertyValue("pathWidth")
                    self.pen.setWidthF(float(width))
                    color.setAlphaF(0.5)
                else: 
                    self.pen.setWidthF(0)
                    color.setAlphaF(1.0)
                    
                self.pen.setColor(color)
                
                
                for line in pathToLineStack(path):
                    scene.addLine(line, self.pen)
                    #TODO: Have the color of the line vary to indicate how far along it is
                
    def setLayers(self, layers):
        """set the layers list which contains the layer list which contians the path instances"""
        self.layers=layers
        self.layerSpin.setRange(0, len(layers)-1)
        self.layerSlider.setRange(0, len(layers)-1)

        maxX=0
        maxY=0
        minX=0
        minY=0
        for layer in layers:
            for path in layer:
                for point in path.getPoints():
                    x = point.x()
                    y= point.y()
                    if x>maxX: maxX=x
                    if y>maxY: maxY=y
                    if x<minX: minX=x
                    if y<minY: maxY=y
        self.layerView.setSceneRect(
                                            QRectF(QPointF(maxX, maxY),
                                                    QPointF(minX, minY)))   
        
        

def pathToLineStack(path):
    """converts a path into a list of QLineF instances"""
    lines =[]
    previouspoint = path.getPoints()[0]
    for point in path.getPoints():
        lines.append(QLineF(previouspoint.qtCoordinates(), point.qtCoordinates()))
        previouspoint=point
    return lines

def sortPathsIntoLayers(pathstack):
    """turns a list of paths into a list of of a list of paths with the same Z value"""
    slices={}
    for path in pathstack:
        z = path.getPoints()[0].z()
        if z in slices.keys(): slices[z].append(path)
        else: slices[z]=[path]

    layers=[]
    for z in sorted(slices.keys()):
        layers.append(slices[z])
    return layers



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    if len(sys.argv)>=2: form = FabFileVisualizer(sys.argv[1])
    else: form=FabFileVisualizer()
    form.show()
    
    app.exec_()

    
