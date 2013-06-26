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
from Point import *
from xml.etree.ElementTree import ElementTree 


class Printer:
    def __init__(self,  type=None):
        self.type= type
        self.axes={}
        self.bays={}
        self.actuators={}
    
    def setAxis(self, id, actuatorId, rPD):
        self.axes[id]={"actuator":actuatorId,  "revolutionsPerDistance":float(rPD)}
        
    def getAxesIds(self):
        return sorted(self.axes.keys())
    
    def addBay(self,id,actuatorId, point,rPV):
        self.bays[id]={"actuator":actuatorId, "location":Point, "revolutionsPerVolume":float(rPV)}
        
    def addActuator(self, id, actuator):
        self.actuators[id]=actuator
    
    def getActuator(self, id):
        return self.actuator[id]
    
    
    def setElectronics(self, numModules, comPort, baudRate):
        pass
        
    def getCountsPerVolume(self):
        counts={}
        for bayId in self.bays.keys():
            bay=self.bays[bayId]
            rPV=bay["revolutionsPerVolume"]
            actuatorId=bay["actuator"]
            counts[bayId]=rPV*self.actuators[actuatorId].getCountsPerRevolution()
        return counts
        
    
    def getCountsPerDistance(self):
        counts={}
        for axisId in self.axes.keys():
            axis=self.axes[axisId]
            rPD=axis["revolutionsPerDistance"]
            actuator=self.actuators[axis["actuator"]]
            cPR=actuator.getCountsPerRevolution()
            counts[axisId]=rPD*cPR

        return counts
            
            
            
class Actuator:
    def __init__(self,  id, type):
        self.id=id
        self.type=type
        self.types=("motor/DC with Encoder",  "motor/DC",  "motor/Stepper",  "motor/Stepper with Encoder")
        self.properties={}
        self.countsPerRevolution=0
    
    def setProperty(self, name, value):
        self.properties[name]=value
        
    def setCountsPerRevolution(self, value):
        self.countsPerRevolution=float(value)
        
    def getCountsPerRevolution (self):
        return self.countsPerRevolution
        
    def getProperty (self, name):
        return self.properties[name]
        
    


def processPrinterConfigFile(configFile):
    doc = ElementTree(file = configFile )
    
    
    type = doc.getroot().attrib["name"]
    printer=Printer(type)
    #Get Printers Actuaors
    for actuatorTag in doc.getroot().getiterator("actuator"):
        id = actuatorTag.attrib["id"]
        type = actuatorTag.attrib["type"]
        actuator=Actuator(id, type)
        
        for propertyTag in actuatorTag.getchildren(): 
            if propertyTag.tag.lower()=="property" :
                actuator.setProperty(propertyTag.attrib["name"], propertyTag.attrib["value"])
    
            if propertyTag.tag.lower()=="countsperrevolution":
                actuator.setCountsPerRevolution(propertyTag.text)
        
        printer.addActuator(id, actuator)
    
    
    #Populate Axes
    for axisTag in doc.getroot().getiterator("axis"):
        printer.setAxis(axisTag.attrib["id"], axisTag.attrib["actuatorId"],axisTag.attrib["revolutionsPerDistance"] )
        
    #Populate Bays
    for bayTag in doc.getroot().getiterator("bay"):
        actuatorId = bayTag.attrib["actuatorId"]
        x=bayTag.attrib["x"]
        y=bayTag.attrib["y"]
        z=bayTag.attrib["z"]
        point=Point(x, y, z)
        rPV=bayTag.attrib["revolutionsPerVolume"]
        id = bayTag.attrib["id"]
        printer.addBay(id,actuatorId,point, rPV)
    
    return printer

