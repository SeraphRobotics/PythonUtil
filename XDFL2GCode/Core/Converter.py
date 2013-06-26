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



import sys
from CommandGenerators import *
from FabFileLoader import processFabFile
from PrinterConfig import processPrinterConfigFile



class Converter:

    def __init__(self,configFile=None,  parent=None):
        self.printer=processPrinterConfigFile(configFile)
        self.commandstack = []
        self.commandGenerator= None 
        self.materials={}
        self.pathstack=[]
        self.materialBays={}
        self.printerType(self.printer.type)
        

    def printerType(self, type):
        type = type.lower()
        if type == "makerbot" or type=="bfb3k":
            self.commandGenerator = MakerbotGCodeGenerator(self.printer)
        elif type == "reprap" or type=="mendel":
            self.commandGenerator = RepRapGCodeGenerator(self.printer)
        else:
            self.commandGenerator = BaseGenerator(self.printer)
        


    def loadFabFile(self, fabfile):
        (self.materials, self.pathstack)=processFabFile(fabfile)
        
        
        
    
    #TODO: enviromental values need to be set.
    def process(self):
        lastpoint=self.pathstack[0].getPoints()[0]
        print "# of points: %i"%len(self.pathstack[0].getPoints())
        lastmaterialname=""
        lasttemp=0
        bayId=0
        
        cmd = self.commandGenerator.configure(self.printer)
        self.commandstack.append(cmd)
        
        for path in self.pathstack:
            material=self.materials[path.getMaterial()]
            
           #TODO: impliment material bay switching.
            if material:
                pathwidth =  float(material.getPropertyValue("pathwidth"))
                pathheight = float(material.getPropertyValue("pathheight"))
                if not pathheight: pathheight = material.getPropertyValue("sliceheight")
                speed=float(material.getPropertyValue("pathspeed"))
                clearance = 0 #float(material.getPropertyValue("clearance"))
                pushout = 0#float(material.getPropertyValue("compressionvolume"))
                suckback = 0#float(material.getPropertyValue("compressionvolume"))
                suckbackdelay = 0 #float(material.getPropertyValue("suckbackdelay"))
                
                
                if material.name != lastmaterialname:
                    vol_per_s =pushout*pathwidth*speed
                    rpv = self.printer.bays[str(bayId)]["revolutionsPerVolume"]
                    rpm = rpv*vol_per_s*60.0
                    cmd = self.commandGenerator.setEnviroment("extrusion_rate", rpm)
                    if cmd: self.commandstack.append(cmd)
                    temp = float(material.getPropertyValue("temperature"))
                    if temp != lasttemp: 
                        cmd=self.commandGenerator.setEnviroment("temperature", temp)
                        lasttemp=temp
                        self.commandstack.append(cmd)
                    
               #This is the Implementation of Clearance between paths
                nextpoint = path.points.pop(0)
                self._doClearance(lastpoint, nextpoint,  clearance, speed)
            
                #Start paths
                cmd = self.commandGenerator.startExtrusionPath()
                if cmd: self.commandstack.append(cmd)
                
                if suckback and pushout:
                   # this does pushout
                    vol = pushout*pathwidth*speed*pushout
                    cmd = self.commandGenerator.extrude(nextpoint, speed, vol, bayId)
                    self.commandstack.append(cmd)
                   # This does part 1 on suckback
                    endpoint = path.points.pop(-1)
                    nexttolast=path.points[-1]
                    d =10*(suckback-suckbackdelay)#speed*(suckback-suckbackdelay)
                    delta = endpoint-nexttolast
                    

                    if d<delta.magnitude(): #TODO: Shouldn't ignore small suck backs. Should wrap around paths. to previous points
                        delta*((delta.magnitude()-d)/delta.magnitude())
                        path.points.append(nexttolast+delta)
                
                
                for point in path.getPoints(): 
                        delta=point-lastpoint
                        vol = pathheight*pathwidth*delta.magnitude()
                        cmd = self.commandGenerator.extrude(point, speed, vol, bayId)
                        self.commandstack.append(cmd)

                    
                if suckback and pushout:
                    #this does that second part of suckback. 
                    vol = -1.0*pushout*pathwidth*speed*(suckback-suckbackdelay)
                    cmd = self.commandGenerator.extrude(endpoint, speed, vol, bayId)
                    self.commandstack.append(cmd)
                    if suckbackdelay:
                        vol = -1.0*pushout*pathwidth*speed*(suckbackdelay)
                        cmd = self.commandGenerator.extrude(endpoint, speed, vol, bayId)
                        self.commandstack.append(cmd)
                    lastpoint=endpoint
                    
                else:
                    lastpoint=point
                lastmaterialname=material.name
                
                
                cmd = self.commandGenerator.endExtrusionPath()
                if cmd: self.commandstack.append(cmd)
                
                
            else:
                for point in path.getPoints(): 
                    speed = path.getSpeed()
                    if not speed: speed = 20 # TODO: impliment path speed defaulting
                    cmd = self.commandGenerator.move(point, speed)
                    self.commandstack.append(cmd)
            
    def printCommands(self):
        for command in self.commandstack: print command
        
        
    def exportToFile(self, filename=None):
            if  not filename: filename="Processed_GCode.txt"
            f= open(filename, "w")
            for cmd in self.commandstack:
                f.write("\n"+cmd)
            f.close()
        
        
    def _doClearance(self, lastpoint, nextpoint, clearance, speed):
       #This is the Implementation of Clearance between paths
        if nextpoint !=lastpoint:
            uppoint = lastpoint + Point(0, 0, clearance)
            topoint = nextpoint + Point(0, 0, clearance)
            m1=self.commandGenerator.move(uppoint, speed)
            m2=self.commandGenerator.move(topoint, speed)
            m3=self.commandGenerator.move(nextpoint, speed)
            self.commandstack.append(m1)
            self.commandstack.append(m2)
            self.commandstack.append(m3)

if __name__ == '__main__':
    control = Converter(sys.argv[1])
    control.loadFabFile(sys.argv[2])
    control.process()
    control.exportToFile(sys.argv[3])
    #control.printCommands()
