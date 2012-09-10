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

def gutter(fabTree, name):
    '''this will gut  a part and replace the inside with the name provided and leave the top and bottom 2 layers untouched'''
    firstZ=round(float(fabTree.find("path").find("point").find("z").text), 4)
    lastZ = round(float(fabTree.findall("path")[-1].find("point").find("z").text), 4)
    layerZ = firstZ
    excludeLayers =  []
    zlist=[]
    
    for path in fabTree.getiterator("path"):
        z = round(float(path.find("point").find("z").text), 4)
        if zlist.count(z) == 0: zlist.append(z)
        
    print zlist
    for i in [0, 1, -2, -1]:excludeLayers.append(zlist[i])
    
    for path in fabTree.getiterator("path"):
        z = round(float(path.find("point").find("z").text), 4)
        if excludeLayers.count(z)==0:
            if z != layerZ: layerZ=z
            else: path.find("materialCalibrationName").text = name

    return fabTree
    
    
def advGutter(fabTree,  name):
    slices={}
    root = fabTree.getroot()
    layer = 0

    for path in fabTree.getiterator("path"):
        z = float(path.find("point").find("z").text)
        if z in slices.keys(): slices[z].append(path)
        else: slices[z]=[path]
    
    
    for z in sorted(slices.keys()):
        if (layer ==0): layer=1
        elif(layer == 1): 
            layer =2
            pointNumber=0
            for path in slices[z]:
                if (pointNumber < 2): pointNumber +=1
                else: 
                    path.find("materialCalibrationName").text = name

        else: layer=0
        
    return fabTree
    
def printPathMaterials(fabTree):
        for path in fabTree.getiterator("path"): print path.find("materialCalibrationName").text
    
if __name__ == "__main__":
    import sys
    fabTree = ElementTree(file = sys.argv[1])
    fabTree = advGutter(fabTree, "Hilighter")
    printPathMaterials(fabTree)
    fabTree.write("gutted.fab")
