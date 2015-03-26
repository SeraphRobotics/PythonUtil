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


class Path:
    def __init__(self, material=None,  speed = None):
        self.material = material
        self.points=[]
        self.speed=speed
    
    def appendPoint(self, point):
        self.points.append(point)
    
    def getPoints(self):
        return self.points
    
    def getMaterial(self):
        return self.material
    
    def setMaterial(self, material):
        self.material=material
        
    def getSpeed(self):
        return self.speed
        

class Material:
    def __init__(self, name):
        self.name = name
        self.properties={}
        pass
        
    
    def setProperty(self, name,  value):
        name = name.lower()
        self.properties[name.lower()]=value
    
    def getPropertyValue(self, name):
        name = name.lower()
        if (self.properties.has_key(name)): return self.properties[name]
        return '0'
    
    def getProperties(self):
        return self.properties.keys()


def processFabFile(fabfile):
    """
    http://www.xml.com/pub/a/2003/02/12/py-xml.html
    http://docs.python.org/library/xml.etree.elementtree.html
    """
    doc = ElementTree(file = fabfile )
    materials={}
    pathstack=[]
    
    root = doc.getroot()
    #Populate Materials
    for materialTag in root.find("palette").findall("material"):
        material = Material(materialTag.find("id").text)
        for propertyTag in materialTag.getchildren(): material.setProperty(propertyTag.tag, propertyTag.text)
        materials[material.name]=material
        
    #Make Path Stack
#    for element in doc.getiterator():
#        if ("path" == element.tag.lower()):
#            matids = element.findall("materialID")
#            print matids
#            if (0!=len(matids)):
#                path=Path(matids[0].text)
#                pathstack.append(path)
#        elif("point"==element.tag.lower()):
#            x = float(element.findall("x")[0].text)
#            y = float(element.findall("y")[0].text)
#            z = float(element.findall("z")[0].text)
#            p=Point(x, y, z)
#            pathstack[-1].appendPoint(p)
            
    cmds = root.find("commands")
    #print len(cmds.findall("path"))
    for pathel in cmds.getiterator("path"):
        #print "path:"
        matids = pathel.findall("materialID")
        matids.extend(pathel.findall("materialid"))
        if (0!=len(matids)):
            path=Path(matids[0].text)
            pathstack.append(path)
            
            for point in pathel.getiterator("point"):
                x = float(point.find("x").text)
                y = float(point.find("y").text)
                z = float(point.find("z").text)
                p=Point(x, y, z)
                #print "Adding point :%f,%f,%f"%(x,y,z)
                pathstack[-1].appendPoint(p)
    
    return (materials, pathstack)


def fabFileVolume(materials, pathstack):
    volume = 0
    for path in pathstack:
        previousPoint = path.getPoints()[0]
        material = materials[path.getMaterial()]
        width = float(material.getPropertyValue('pathWidth'))
        hieght = float(material.getPropertyValue("pathHieght"))
        
        if hieght < 0.001: hieght = width 
        for point in path.getPoints():
            delta = point - previousPoint
            volume += width*hieght*delta.magnitude()
        
    return volume
    
def fabFilePrintTime(materials, pathstack):
    time = 0
    
    for path in pathstack:
        previousPoint = path.getPoints()[0]
        material = materials[path.getMaterial()]
        speed= float(material.getPropertyValue('pathSpeed'))

        for point in path.getPoints():
            delta = point - previousPoint
            time += delta.magnitude()/speed
        
    return time

    
if __name__ == "__main__":
    import sys
    file = sys.argv[1]
    (materials, pathstack) = processFabFile(file)
    print fabFileVolume(materials, pathstack),  "mm^3"
    time  = fabFilePrintTime(materials, pathstack)
    print time,  "s or ",  time/60.0,  "min"
