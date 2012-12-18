from PyQt4.QtCore import *
from PyQt4.QtGui import *

from XDFLVisualizer.XDFLVisualizer import XDFLMCU as XDFLer
from SliceStackVisualizer.SliceStackMCU import SliceStackMCU as SliceStacker
from SegmentVisualizer.SegmentStackMCU import SegmentStackMCU as Segmenter
from LoopVisualizer.LoopStackMCU import LoopStackMCU as Looper
from xml.etree.ElementTree import ElementTree, Element 

if __name__ == "__main__":
    import sys
    
    app  = QApplication(sys.argv)
    fileTree = ElementTree(file = sys.argv[1])
    root = fileTree.getroot()
    roottag = root.tag.lower()
    if("stack"==roottag):
        x=SliceStacker(sys.argv[1])
    elif("segments"==roottag):
        x=Segmenter(sys.argv[1])
    elif("loops" == roottag):
        x=Looper(sys.argv[1])
    elif("xdfl"==roottag):
        x=XDFLer(sys.argv[1])
    app.exec_()