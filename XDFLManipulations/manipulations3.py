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
import xml.etree.ElementTree as etree
from math import cos, sin, pi

def transformPoint(transformation, point):
	x, y, z = point.find("x").text, point.find("y").text, point.find("z").text
	point.find("x").text, point.find("y").text, point.find("z").text  = transformation(float(x), float(y), float(z))

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
    '''This will threshold a fabFile element tree and return the tree'''
    for path in fabTree.getiterator("path"):
        zValue = float(path.find("point").find("z").text)
        if zValue <= threshold: fabTree.getroot().remove(path)
    return fabTree

def getPoints(mid, fabTree):

	# Return a list of points satisfying the material ID code "mid": 
	# If mid is negative, return all points in all paths
	# If mid is 0, only return points in transition paths
	# If mid is positive, only return points from material paths and voxels

	points = []
   	for path in fabTree.getiterator("path"):
		matidel = path.find("materialID")
		if mid < 0: 
			for point in path.findall("point"): points.append(point)
		elif mid == 0 and (matidel == None):
			for point in path.findall("point"): points.append(point)
		elif (not matidel == None) and mid == float(matidel.text): 
			for point in path.findall("point"): points.append(point)		

	if mid > 0: 
		for voxel in fabTree.getiterator("voxel"): 
			if float(voxel.find("materialID").text) == mid:
				points.append(voxel)

	return points

def translate(fabTree, dx=0, dy=0, dz=0, mid=-1):
	
	translate = lambda x,y,z: (str(x + dx), str(y + dy), str(z + dz))
	
    # This will translate a fabFile element tree and return the tree
	points = getPoints(mid, fabTree)
	for p in points: transformPoint(translate, p)
	return fabTree

def scale(fabtree, dx=0, dy=0, dz=0, mid=-1):
	
	scale = lambda x,y,z: (str(x * dx), str(y * dx), str(z * dz))

	#This will scale a fabFile element tree and return the tree
	points = getPoints(mid, fabTree)
	for p in points: transformPoint(scale, p)
	return fabTree

def rotate(fabTree, theta, mid=-1):
	thetaInRadians = theta/180*pi
	rotate = lambda x, y, z: (str(cos(thetaInRadians)*x - sin(thetaInRadians)*y), 
             str(sin(thetaInRadians)*x + cos(thetaInRadians)*y), str(z))

	#This will rotate a fabFile element tree and return the tree
	points = getPoints(mid, fabTree)
	for p in points: transformPoint(rotate, p)        
	return fabTree
    
def parity(fabTree, mid=-1):
	parity = lambda x, y, z: (str(y), str(x), str(z))

    # This will translate a fabFile element tree and return the tree
	points = getPoints(mid, fabTree)
	for p in points: transformPoint(parity, p)
	return fabTree
             
def dimensions(fabTree, mid=None):
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
    
    
def startpath(fabTree, number):
    root = fabTree.getroot()
    cmd = root.find("commands")
    i = 0;
    for path in fabTree.getiterator("path"):
        i= i+1
        if (i < number):
            print "removed ",i 
            cmd.remove(path)
    return fabTree


if __name__ == '__main__':
	import sys
	todo = sys.argv[1]

	def print_error():
		print "Incorrect number of arguments"
		print todo
	 	print sys.argv

	def writeTree(output_file, tree):

		f = open(output_file, 'w')
		f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?> \n")
		string = etree.tostring(tree.getroot())
		f.write(string)
		f.close()

	if todo== "help":
		print "\ntranslate - manipulations.py translate 'file name' x y z 'write name'"
		print "\nthreshold  - manipulations.py threshold 'file name' ('write name')"
		print "\nrotate - manipulations.py rotate 'file name' theta 'write name'"
		print "\nparity - manipulations.py parity 'file name' 'write name'"
		print "\nstartpath - manipulations.py  startpath 'file name' index 'write name' "
		print "\nscale - manipulations.py scale 'filename' x y z 'write name' "
		
	else:
		fabTree = ElementTree(file = sys.argv[2])
		for el in fabTree.iter(): el.tag = el.tag.lower()
    
	if todo == "threshold":
        #threshold fabFile NewFab
		fabTree = threshold(fabTree)
		if len(sys.argv)>3: fabTree.write(sys.argv[3])
		else: writeTree(sys.argv[2], fabTree)	
        
	elif todo == "translate":
		#translate fabfile x yz
		if len(sys.argv)>6:
			x = float(sys.argv[3])
			y = float(sys.argv[4])
			z = float(sys.argv[5])
			fabTree=translate(fabTree, x, y, z)
			writeTree(sys.argv[6], fabTree)	
		else: print_error()
    
	elif todo == "rotate":
		# rotate XDFL file 
		if len(sys.argv)>4:
			theta = float(sys.argv[3])
			fabTree=rotate(fabTree, theta)
			writeTree(sys.argv[4], fabTree)	
		else: print_error()

	elif todo == "parity":
        # rotate XDFL file 
		print "parity"
		fabTree=parity(fabTree)
		writeTree(sys.argv[3], fabTree)	

	elif todo == "dimensions":
		(minvalues,maxvalues) = dimensions(fabTree)
		print minvalues,maxvalues

	elif todo == "startpath":
		number = float(sys.argv[3])
		fabTree=startpath(fabTree,number)
		writeTree(sys.argv[4], fabTree)	
        
	elif todo == "scale":
        #translate fabfile x yz
		if len(sys.argv)>6:
			x = float(sys.argv[3])
			y = float(sys.argv[4])
			z = float(sys.argv[5])
			fabTree=scale(fabTree, x, y, z)
			writeTree(sys.argv[6], fabTree)	
		else: print_error()

