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
from math import cos, sin, pi

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

def threshold(fabTree, threshold=0):
    "This will threshold a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        zValue = float(path.find("point").find("z").text)
        if zValue <= threshold: fabTree.getroot().remove(path)
    return fabTree

    
def translate(fabTree, dx=0, dy=0, dz=0,name=None):
    axes = ["x", "y", "z"]
    values = [dx, dy, dz]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        matidel = path.find("materialID")
        ##if (type(None) == type(matidel)):break
        ##if (name and matidel.text !=name):break
        for point in path.findall("point"):
            for i in range(0, 3):
                el = point.find(axes[i])
                if(type(None)==type(el)):
                    print "no", axes[i]
                else:
                    val = float(el.text)
                    el.text = "%f"%(val+values[i])
                    ##if (values[i]): print axes[i], i
                    ##print  axes[i], val,"to", float(el.text)
    return fabTree

def rotate(fabTree, theta,name=None):
    thetaInRadians = theta/180*pi
    axes = ["x", "y", "z"]
    values = [0, 0, 0]
    newvalues = [0, 0,0]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        ## matidel = path.find("materialID")
        ##if (type(None) == type(matidel)):break
        ##if (name and matidel.text !=name):break
        for point in path.findall("point"):
            elx = point.find(axes[0])
            ely = point.find(axes[1])
            values[0] = float(elx.text)
            values[1] = float(ely.text)
            
            newvalues[0] = cos(thetaInRadians)*values[0]-sin(thetaInRadians)*values[1]
            newvalues[1] = sin(thetaInRadians)*values[0]+cos(thetaInRadians)*values[1]                

            elx.text = "%f"%(newvalues[0])
            ely.text = "%f"%(newvalues[1])
            
            
    return fabTree
    
    
    
def parity(fabTree, name=None):
    axes = ["x", "y", "z"]
    values = [0, 0, 0]
    newvalues = [0, 0,0]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        ## matidel = path.find("materialID")
        ##if (type(None) == type(matidel)):break
        ##if (name and matidel.text !=name):break
        for point in path.findall("point"):
            elx = point.find(axes[0])
            ely = point.find(axes[1])
            values[0] = float(elx.text)
            values[1] = float(ely.text)
            
            newvalues[0] = values[1]
            newvalues[1] = values[0]                

            elx.text = "%f"%(newvalues[0])
            ely.text = "%f"%(newvalues[1])
            
            
    return fabTree
    
def dimensions(fabTree, name=None):
    axes = ["x", "y", "z"]
    minvalues = [0, 0, 0]
    maxvalues = [0, 0,0]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        ## matidel = path.find("materialID")
        ##if (type(None) == type(matidel)):break
        ##if (name and matidel.text !=name):break
        for point in path.findall("point"):
            for i in range(0, 3):
                el = point.find(axes[i])
                if(type(None)==type(el)):
                    print "no", axes[i]
                else:
                    val = float(el.text)
                    if (val > maxvalues[i]): maxvalues[i]=val
                    if (val < minvalues[i]): minvalues[i]=val
            
            
    return (minvalues,maxvalues)
    
    




if __name__ == '__main__':
    import sys
    todo = sys.argv[1]
    
    if todo== "help":
        print "\ntranslate - manipulations.py traslate 'file name' x y z "
        print "\ntheshold  - manipulations.py threshold 'file name' ('write name')"
    else: fabTree = ElementTree(file = sys.argv[2])
    
    
    if todo == "threshold":
        #threshold fabFile NewFab
        fabTree = threshold(fabTree)
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
            print "Incorrect number of arguments"
            print todo
            print sys.argv
    
    elif todo == "rotate":
        # rotate XDFL file 
        if len(sys.argv)>2:
            theta = float(sys.argv[3])
            fabTree=rotate(fabTree, theta)
            fabTree.write(sys.argv[2])
        else:
            print "Incorrect number of arguments"
            print todo
            print sys.argv

    elif todo == "parity":
        # rotate XDFL file 
        print "parity"
        fabTree=parity(fabTree)
        fabTree.write(sys.argv[2])
    elif todo == "dimensions":
        (minvalues,maxvalues) = dimensions(fabTree)
        print minvalues,maxvalues


