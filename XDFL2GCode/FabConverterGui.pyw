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
from Gui.ui_FabConverter import *
from Gui.ui_About import *
from Core.Converter import Converter

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
 
class FabConverter(QMainWindow, Ui_FabConverter):
    def __init__(self):
        super(FabConverter, self).__init__()
        self.fabFile=None
        self.setupUi(self)
        
        self.connect(self.loadFabFileButton, SIGNAL("clicked()"), self.loadFabFile )
        self.connect(self.repRapButton, SIGNAL("clicked()"), lambda: self.loadPrinter("RepRap") )
        self.connect(self.makerbotButton, SIGNAL("clicked()"),lambda: self.loadPrinter("makerbot") )
        self.connect(self.rapManButton, SIGNAL("clicked()"), lambda: self.loadPrinter("BFB3k") )
        self.connect(self.saveAsButton, SIGNAL("clicked()"), self.saveGCode)
        self.connect(self.aboutAction, SIGNAL("triggered()"), self.showAbout)
    
    def loadFabFile(self):
        self.fabFileEdit.clear()
        fileName = QFileDialog.getOpenFileName(None,"Select XDFL File", "", "XDFL Files (*.xdfl)")
        self.fabFile=fileName
        f = QFile(fileName)
        f.open(QIODevice.ReadOnly) 
        stream = QTextStream(f)
        self.fabFileEdit.setDisabled(True)
        self.loadFabFileButton.setDisabled(True)
        self.loadFabFileButton.repaint()
        while not stream.atEnd(): 
            self.fabFileEdit.append(stream.readLine())
        self.fabFileEdit.setEnabled(True)
        f.close()
        
    def loadPrinter(self, type):
            # this is not a robust way of getting this to work
            if self.fabFile:
                filename = "Core/%s.xml"%type
                converter = Converter(filename)
                converter.loadFabFile(self.fabFile)
                converter.process()
                self.gcodeTextEdit.clear()
                for line in converter.commandstack:
                    self.gcodeTextEdit.append(line)
                self.printer=filename
            else:
                QMessageBox.warning(self, "Load XDFL File", "Please load a '.XDFL' file",  QMessageBox.Ok)
                
    def saveGCode(self):
        if self.printer and self.fabFile:
            fileName = QFileDialog.getSaveFileName(None,"Select G-Code file name")
            f = QFile(fileName)
            f.open(QIODevice.WriteOnly)
            stream = QTextStream(f)
            stream << self.gcodeTextEdit.toPlainText()
            f.close()
        
    def showAbout(self):
        aboutDialog=AboutDialog()
        aboutDialog.exec_()
        
    
class AboutDialog(QDialog,  Ui_aboutDialog):
     def __init__(self):
        super(AboutDialog, self).__init__()
        self.setupUi(self)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FabConverter()
    form.show()
    
    app.exec_()
     
