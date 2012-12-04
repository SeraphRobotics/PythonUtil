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


from xml.etree.ElementTree import ElementTree 
import math
from orthoticTrim import *

def merge(fabTree, fabTree2):
    root = fabTree.getroot()
    for path in fabTree2.getiterator("path"):
        root.append(path)
    return sortIntoLayers(fabTree)

def sortIntoLayers(fabTree):
    slices={}
    root = fabTree.getroot()
    for path in fabTree.getiterator("path"):
        z = float(path.find("point").find("z").text)
        if z in slices.keys(): slices[z].append(path)
        else: slices[z]=[path]
        root.remove(path)

    for z in sorted(slices.keys()):
        for path in slices[z]:
            root.append(path)
    return fabTree

def thresholdPaths(fabTree, threshold=0):
    "This will threshold a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        zValue = float(path.find("point").find("z").text)
        if zValue <= threshold: fabTree.getroot().remove(path)
    return fabTree

def thresholdPoints(fabTree, threshold=0):
    "This will threshold a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        for point in path.getiterator("point"):
            zValue = float(point.find("z").text)
            if zValue <= threshold: path.remove(point)
        if (len(path.findall("point"))<2):fabTree.getroot().remove(path)
    return fabTree

def rotateY(fabTree,angle):
    angle = math.pi/180.0*angle
    axes = ["x","y","z"]
    
    for path in fabTree.getiterator("path"):
        for point in path.getiterator("point"):
            els = []
            point_array = []
            for i in range(0,3):
                els.append(point.find(axes[i]))
                point_array.append(float(els[i].text))
            ###ROTATION ABOUT Y AXIS
            xprime = math.cos(angle)*point_array[0] + math.sin(angle)*point_array[2]
            yprime = point_array[1]
            zprime = -math.sin(angle)*point_array[0] + math.cos(angle)*point_array[2]
            primes = [xprime,yprime,zprime]
            
            for i in range(0,3):
                els[i].text="%f"%primes[i]
    
    return fabTree
            
    
def translate(fabTree, dx=0, dy=0, dz=0, name=None):
    axes = ["x", "y", "z"]
    values = [dx, dy, dz]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        if (name and path.find("materialCalibrationName").text !=name):break
        for point in path.findall("point"):
            for i in range(0, 3):
                el = point.find(axes[i])
                val = float(el.text)
                el.text = "%f"%(val+values[i])
    return fabTree

    
    

def startPath(fabTree, pathnumber):
    i=0
    root = fabTree.getroot()
    for path in fabTree.getiterator("path"):
        if (i<pathnumber):
            i+=1
            root.remove(path)
            print "removed path",i

        
    return fabTree
    


if __name__ == '__main__':
    import sys
    todo = sys.argv[1]
    
    if todo== "help":
        print "\ntranslate   -  manipulations.py traslate 'file name' x,y,z "
        print "\ntheshold - manipulations.py threshold 'file name' ('write name')"
        print "\nmerge - manipulations.py merge 'file1' 'file2' ('write name')"
    else: fabTree = ElementTree(file = sys.argv[2])
    
    
    if todo == "merge":
        # merge fab1 fab2 (newFab)
        if len(sys.argv)>3:
            fabTree2 = ElementTree(file = sys.argv[3])
            fabTree = merge(fabTree, fabTree2)
            
        if len(sys.argv)>4: fabTree.write(sys.argv[4])
        else: fabTree.write(sys.argv[2])
        
    elif todo == "threshold":
        #threshold fabFile NewFab
        fabTree = thresholdPaths(fabTree)
        if len(sys.argv)>3:fabTree.write(sys.argv[3])
        else:fabTree.write(sys.argv[2])
        
    elif todo == "translate":
        #translate fabfile x yz
        if len(sys.argv)>5:
            x = float(sys.argv[3])
            y = float(sys.argv[4])
            z = float(sys.argv[5])
            fabTree=translate(fabTree, x, y, z)
            fabTree.write(sys.argv[2])
        else:
            print "Incorrect number of arguments length arguments was", len(sys.argv)
            print "arguments were", sys.argv[3],sys.argv[4],sys.argv[5]
 
    elif todo == "startpath":
        pathnum = int(sys.argv[3])
        fabTree=startPath(fabTree,pathnum)
        fabTree.write(sys.argv[2])
        
    elif todo =="thresholdpoints":
        thresholdZ = float(sys.argv[3])
        fabTree = thresholdPoints(fabTree,thresholdZ)
        fabTree.write(sys.argv[2])
        
    elif todo=="rotateY":
        angle = float(sys.argv[3])
        fabTree = rotateY(fabTree,angle)
        fabTree.write(sys.argv[2])
        
    elif todo=="orthotic":
        angle = float(sys.argv[3])
        translateZ = float(sys.argv[4])
        pathWidth = float(sys.argv[5])
#        thresholdZ = float(sys.argv[5])
        fabTree = rotateY(fabTree,angle)
        fabTree = translate(fabTree,0,0,translateZ)
        fabTree = trimSidesAndBottom(fabTree)
        
        fabTree = solveHolesInLayers(fabTree,pathWidth,  0)
#        fabTree = thresholdPoints(fabTree,thresholdZ)
        if (len(sys.argv)>6):
            fabTree.write(sys.argv[6])
        else:
            fabTree.write(sys.argv[2])
        


