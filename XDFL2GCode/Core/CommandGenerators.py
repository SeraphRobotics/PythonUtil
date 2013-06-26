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

class BaseGenerator(object):
    def __init__(self, printer):
        self.lastpoint=Point(0, 0, 0)
        self.printer=printer
        
    def move(self, point, speed):
        self.lastpoint=point
        return "Move to (%f,%f,%f)"%(point.getX(), point.getY(), point.getZ()) 
    
    def extrude(self, point, speed, vol, bayId):
        self.lastpoint=point
        return "Extrude to (%f,%f,%f) with %f ml from Bay %i "%(point.getX(), point.getY(), point.getZ(), vol/1000.0, int(bayId)) 
    
    def configure (self,  printer):
        # TODO: generate configuration string from printer   
        return "Configure"
        
    def toOrigin(self, speed, point=None):
        return "Move to Origin"
        
    def dwell(self, timeinms):
        return "Dwell %i"%int(timeinms)
        
    def setPosition(self, point, extrudePosition=None):
        return "Set Position (%f,%f,%f)"%(point.getX(), point.getY(), point.getZ())
        
    def setEnviroment(self, varName, varValue):
        return "%s set to %f"%(varName, float(varValue) )

    def get(self, varName):
        return "get %s"%varName

    def stop(self):
        return "stop"
        
    def emergancyStop(self):
        return "EMERGANCY STOP"
    
    def changeBay(self, bayId):
        return "change bay to %i"%int(bayId)
        
    def endExtrusionPath(self):
        return ""
        
    def startExtrusionPath(self):
        return ""
    

    
    


class CustomBoardGenerator(BaseGenerator):
   
    def move(self, point, speed):
        #(sx, sy, sz)=returnSpeeds(point, self.lastpoint, speed)
        time = returnTime(point, self.lastpoint, speed)
        # TODO: return movement command formatted for Stephan
        deltas=(point.getX(), point.getY(), point.getZ())
        self.lastpoint=point
        counts=[]

        for i in range(0, len(self.printer.getAxesIds())): 
            cPD=self.printer.getCountsPerDistance()[self.printer.getAxesIds()[i]]
            counts.append(deltas[i]*cPD)
           
        return 'Move to [%f %f %f] in %f ms'%(counts[0], counts[1],counts[2],  time)
        
    def toOrigin(self, speed, point=None):
        if point == None: point=Point(0, 0, 0)
        return self.move(point, speed)

    

class RepRapGCodeGenerator(BaseGenerator):

    def __init__(self, printer):
        super(RepRapGCodeGenerator, self).__init__(printer)
        self.lastBay=0
        self.ExtrusionPosition=0
        
    def configure(self, printer):
        #TODO Finish Gcode Configuration
        inMM = "G21 "
        absolutePositioning="G90 "
        PWM = "M113 S%f"
        stepper = "M108" ##Sets the PWM of the extruder's stepper motor. This controls its torque
        
        return inMM+absolutePositioning

    def move(self, point, speed):
        (x, y, z)=(point.getX(), point.getY(), point.getZ())
        speed=speed*60.0
        self.lastpoint=point
        return "G1 X%f Y%f Z%f F%f"%(x, y, z, speed)

    def extrude(self, point, speed, vol, bayId):
        #extrudes a volume of material for a given motion command and material
        bayId= str(bayId)
        (x, y, z)=(point.getX(), point.getY(), point.getZ())
        speed = speed*60.0
        rpv = self.printer.bays[bayId]["revolutionsPerVolume"]
        #FIXME need to get convert Revolutions to distance
        self.lastpoint=point
        self.ExtrusionPosition = self.ExtrusionPosition+vol*rpv
        cmd = "G1 X%f Y%f Z%f E%f F%f"%(x, y, z, self.ExtrusionPosition, speed)
        if bayId != self.lastBay: 
            cmd = self.changeBay(bayId)+" "+cmd
            self.lastBay=bayId

        return cmd

    def toOrigin(self, speed, point=None):
        command="G28 "
        if point == None: point=Point(0, 0, 0)
        if point.getX(): command +="X%f "%point.getX()
        if point.getY(): command +="Y%f "%point.getY()
        if point.getZ(): command +="Z%f"%point.getZ()
        return command

    def dwell(self, timeinms):
        return "G4 P%i"%int(timeinms)
        
    def setPosition(self, point, extrudePosition=None):
        command="G92"
        if point.getX(): command +="X%f "%point.getX()
        if point.getY(): command +="Y%f "%point.getY()
        if point.getZ(): command +="Z%f"%point.getZ()
        if extrudePosition: command+="E%f"%extrudePosition
        return command
        
    def setEnviroment(self, varName, varValue):
        if "bay_temperature"==varName: 
            return "M109 S%f"%float(varValue)
        elif "cooling"==varName: 
            if varValue: return "M106"
            else: return "M107"
        elif "temperature"==varName:
            return "M115 S%f"%float(varValue)
            
    
    def get(self, varName):
        if "bay_temperature"==varName: 
            return "M105"
    
    def stop(self):
        return "M0"
    
    def emergancyStop(self):
        return "M112"
    
    def changeBay(self, bayId):
        return "T%i"%int(bayId)
        

class MakerbotGCodeGenerator(RepRapGCodeGenerator):
    '''
    M101 Turn extruder on Forward.
    M103 Turn extruder off.
    M104 S145.0 Set target temperature to 145.0 C.
    M108 S400 Set Extruder speed to S value/10 = 40rpm.
    '''
    def __init__(self, printer):
        super(MakerbotGCodeGenerator, self).__init__(printer)
##        self.extrusionspeed=0.0
        
    def setEnviroment(self, varName, varValue):
        if "bay_temperature"==varName: 
            return "M109 S%f"%float(varValue)
        elif "cooling"==varName: 
            if varValue: return "M106"
            else: return "M107"
        elif "temperature"==varName:
            return "M104 S%f"%float(varValue)
        elif "extrusion_rate" == varName:
            return "M108 S%f"%float(varValue*10.0)
            
    def extrude(self, point, speed, vol, bayId):
        #extrudes a volume of material for a given motion command and material
        bayId= str(bayId)
##        delta = point-self.lastpoint
        cmd = self.move(point, speed)
## This was an attempt to have extruder speed set dynamically
##        rpv = self.printer.bays[bayId]["revolutionsPerVolume"]
##        
##        time  = delta.magnitude()*speed
##        if time:
##            extrusionspeed = (vol*rpv)/time
##            if self.extrusionspeed != extrusionspeed:
##                cmd = "M108 %f\n"%(extrusionspeed*10.0)  +cmd
##                self.extrusionspeed = extrusionspeed
        
        if bayId != self.lastBay: 
            cmd = self.changeBay(bayId)+" "+cmd
            self.lastBay=bayId
        return cmd
        
    def endExtrusionPath(self):
        return "M103"
        
    def startExtrusionPath(self):
        return "M101"
        
