from distutils.core import setup  
import py2exe  
  
setup(windows=['FabFileVisualizer.py'], options={"py2exe": {"includes": ["sip", "PyQt4.QtGui"]}}) 
