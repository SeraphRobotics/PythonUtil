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
from math import sqrt,  pow
from PyQt4.QtCore import *

class Point(QPointF):
    ''' '''
    def __init__(self, x=0, y=0, z=0,  parent=None):
        QPointF.__init__(self)
        self.setX(x)
        self.setY(y)
        self.zValue=float(z)
       
        
        
    def magnitude(self):
        return sqrt(self.x()*self.x()+self.y()*self.y()+self.z()*self.z())
        
    def setZ(self, value):
        self.zValue=value
        
    def z(self):
        return self.zValue
        
    def qtCoordinates(self):
        "returns a xy partity transform of the point to map to the GUI"
        return Point(self.y(), self.x(), self.z())
        
    
    def __add__(self, point):
        x = self.x() + point.x()
        y = self.y() + point.y()
        z = self.z() + point.z()
        return Point(x, y, z)
    
    def __sub__(self, point):
        x = self.x() - point.x()
        y = self.y() - point.y()
        z = self.z() - point.z()
        return Point(x, y, z)   
    
    def __mul__(self, value):
        self.setX(self.x()*value)
        self.setY(self.y()*value)
        self.setZ(self.z()*value)
        
    def __div__(self, value):
        self.setX(self.x()/value)
        self.setY(self.y()/value)
        self.setZ(self.z()/value)
    
    def __eq__(self, point):
        return ((self.x()-point.x())==(self.y()-point.y())==(self.z()-point.z()))

    
def returnSpeeds(point1, point2, pathspeed):
    delta = point2 - point1
    if (delta.magnitude()==0): return (0, 0, 0)
    xspeed = abs(delta.x())*pathspeed/delta.magnitude()
    yspeed = abs(delta.y())*pathspeed/delta.magnitude()
    zspeed = abs(delta.z())*pathspeed/delta.magnitude()
    return (xspeed, yspeed,  zspeed)
    
def returnTime(point1, point2, pathspeed):
    delta = point2 - point1
    if (pathspeed ==0): return 0
    return delta.magnitude()/pathspeed
    

