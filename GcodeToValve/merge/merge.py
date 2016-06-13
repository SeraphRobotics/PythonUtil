#!/usr/bin/env python

import math
import os
import re
import sys
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree

### DO NOT CHANGE UNLESS YOUR SURE
XMLFile  = "Files.xml"
OutFile = "Merged.gcode"
RaiseCmd = "G91\nG1 Z%0.0f F%0.0f\nG90\n"
#####

class Layer:
    displacement = 1
    valve = 2
    
    def __init__(self,z):
        self.stackz=z
        self.acutalz=z
        self.cmds=[]
        self.type=Layer.valve

        
def findMinMax(layerlist):
    max = [-300,-300]
    min = [300,300]
    for layer in layerlist :
        for line in layer.cmds:
            xy_move_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
            if xy_move_match:
                m1 = [0]*3
                for j in range(0,3):
                    group = xy_move_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            m1[2]=xy_move_match.groups()[j+1]
                            break
                        else:
                            m1[j]=float(group)
                
                if(min[0]>m1[0]):min[0]=m1[0]
                if(min[1]>m1[1]):min[1]=m1[1]
                if(max[0]<m1[0]):max[0]=m1[0]
                if(max[1]<m1[1]):max[1]=m1[1]

    return (min,max)
                
        
def processFileIntoLayers(filename,isplastic,verbose):
    infile = open(filename)
    cmd_group =[]
    newlayer=Layer(0)
    if(isplastic == True): newlayer.type = Layer.displacement
    
    for line in infile:
        z_move_match = re.match(r'^G1 Z([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())

        if z_move_match:
            cmd_group.append(newlayer)
            if verbose: print "Z_move: ", z_move_match.groups()
            z1 = [0]*2
            for j in range(0,2):
               group = z_move_match.groups()[j]
               if not (type(group)==type(None)):
                    if "f" in group.lower():
                        z1[1]=z_move_match.groups()[j+1]
                        break
                    else:
                        z1[j]=float(group)
            newlayer=Layer(z1[0])
            
        if(isplastic==True): newlayer.type = Layer.displacement
        #else: newlayer.stackz+=10;
        newlayer.cmds.append(line)

    cmd_group.append(newlayer)
    infile.close()
    return cmd_group   ## A LIST OF LAYERS

def parity(layerlist, verbose=False):
    for layer in layerlist :
        out_line_list=[]
        for line in layer.cmds:
            xy_move_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
            z_move_match = re.match(r'^G1 Z([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
            extrude_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) E([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                             line.rstrip())
            topcoat_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) Z([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                             line.rstrip())
            if topcoat_match:
                if verbose: print "extrude: ", topcoat_match.groups()
                p2 =[0]*4
                
                for j in range(0,4):
                    group = topcoat_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            p2[3]=topcoat_match.groups()[j+1]
                            break
                        else:
                            p2[j]=float(group)
                speed=""
                if p2[3]>0:
                    speed = " F%f"%float(p2[3])
                
                newline = "G1 X%f Y%f Z%f%s\n"%(p2[1],p2[0],p2[2],speed)
                out_line_list.append(newline)
            
            elif extrude_match:

                if verbose: print "extrude: ", extrude_match.groups()
                p2 =[0]*4
                
                for j in range(0,4):
                    group = extrude_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            p2[3]=extrude_match.groups()[j+1]
                            break
                        else:
                            p2[j]=float(group)
                speed=""
                if p2[3]>0:
                    speed = " F%f"%float(p2[3])
                
                newline = "G1 X%f Y%f E%f%s\n"%(p2[1],p2[0],p2[2],speed)
                out_line_list.append(newline)
                
                
            elif xy_move_match:
                if verbose: 
                    print "move: ", xy_move_match.groups()
                
                m1 = [0]*3
                for j in range(0,3):
                    group = xy_move_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            m1[2]=xy_move_match.groups()[j+1]
                            break
                        else:
                            m1[j]=float(group)
                
                speed = ""
                if m1[2]>0: 
                    speed = " F%f"%float(m1[2])

                newline = "G1 X%f Y%f%s\n"%(m1[1],m1[0],speed)
                out_line_list.append(newline)
                
            elif z_move_match:
                if verbose: print "Z_move: ", z_move_match.groups()

                z1 = [0]*2
                for j in range(0,2):
                    group = z_move_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            z1[1]=float(z_move_match.groups()[j+1])
                            break
                        else:
                            z1[j]=float(group)        

                layer.actualz = z1[0]
                newline = "G1 Z%f F%f\n"%(z1[0],z1[1])
                out_line_list.append(newline)
                
            else:
                if verbose: print line
                out_line_list.append(line)
        layer.cmds = out_line_list

def translate(layerlist, delta, verbose=False, shiftlayer=False):
    for layer in layerlist :
        out_line_list=[]
        if shiftlayer: layer.stackz = layer.stackz+delta[2]
        for line in layer.cmds:
            xy_move_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
            z_move_match = re.match(r'^G1 Z([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
            extrude_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) E([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                             line.rstrip())
            topcoat_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) Z([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                             line.rstrip())
            fan_match = re.match("r'^M106 S([-\d\.]+)",line.rstrip())
            if topcoat_match:
                if verbose: print "extrude: ", topcoat_match.groups()
                p2 =[0]*4
                
                for j in range(0,4):
                    group = topcoat_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            p2[3]=topcoat_match.groups()[j+1]
                            break
                        else:
                            p2[j]=float(group)
                speed=""
                if p2[3]>0:
                    speed = " F%f"%float(p2[3])
                p2[0] = delta[0] + p2[0]
                p2[1] = delta[1] + p2[1]
                p2[2] = delta[2] + p2[2]
                newline = "G1 X%f Y%f Z%f%s\n"%(p2[0],p2[1],p2[2],speed)
                out_line_list.append(newline)
            
            elif extrude_match:

                if verbose: print "extrude: ", extrude_match.groups()
                p2 =[0]*4
                
                for j in range(0,4):
                    group = extrude_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            p2[3]=extrude_match.groups()[j+1]
                            break
                        else:
                            p2[j]=float(group)
                speed=""
                if p2[3]>0:
                    speed = " F%f"%float(p2[3])
                p2[0] = delta[0] + p2[0]
                p2[1] = delta[1] + p2[1]
                
                newline = "G1 X%f Y%f E%f%s\n"%(p2[0],p2[1],p2[2],speed)
                out_line_list.append(newline)
                
                
            elif xy_move_match:
                if verbose: 
                    print "move: ", xy_move_match.groups()
                
                m1 = [0]*3
                for j in range(0,3):
                    group = xy_move_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            m1[2]=xy_move_match.groups()[j+1]
                            break
                        else:
                            m1[j]=float(group)
                
                speed = ""
                if m1[2]>0: 
                    speed = " F%f"%float(m1[2])
                m1[0] = delta[0] + m1[0]
                m1[1] = delta[1] + m1[1]
                newline = "G1 X%f Y%f%s\n"%(m1[0],m1[1],speed)
                out_line_list.append(newline)
                
            elif z_move_match:
                if verbose: print "Z_move: ", z_move_match.groups()

                z1 = [0]*2
                for j in range(0,2):
                    group = z_move_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            z1[1]=float(z_move_match.groups()[j+1])
                            break
                        else:
                            z1[j]=float(group)        

                z1[0]= z1[0] + delta[2]
                layer.actualz = z1[0]
                if(z1[1]>600): z1[1]=600
                newline = "G1 Z%f F%f\n"%(z1[0],z1[1])
                out_line_list.append(newline)
                
            elif fan_match:
                if verbose:
                    print "temp: ",fan_match.groups()
                m1 = [0]
                
                out_line_list.append("M106 S100");
            else:
                if verbose: print line
                out_line_list.append(line)
        layer.cmds = out_line_list

def mergeFromXML(infilename, outfilename, verbose, debug):
    fabTree = ElementTree(file = infilename)
    for el in fabTree.iter(): el.tag = el.tag.lower()
    root = fabTree.getroot()

    clNode = root.find("clearance")
    clearance = None
    if clNode is not None: clearance = float(clNode.text)
    zspeed = 600
    zNode = root.find("clearanceSpeed")
    if zNode: zspeed = float(zNode.text)*60
    print "Clearance: ",clearance
    print "Speed: ",zspeed
    
    def nodeToFileOffset(node):
        file = node.find("filename").text
        zoffset = float(node.find("zoffset").text)
        ztranslate = float(node.find("ztranslate").text)
        xcenter= float(node.find("xcenter").text)
        ycenter = float(node.find("ycenter").text)
        return [file,zoffset,ztranslate,xcenter,ycenter]
    
    ## Process file 
    fileNodes = root.findall("file")
   
    mergelist = []

    
    ## make Pad layer lists
    
    for gfilenode in fileNodes:
        [gfilefile,gfilez,locationz,gfile_x,gfile_y] = nodeToFileOffset(gfilenode)
        gfile_list = processFileIntoLayers(gfilefile,False,verbose)
        (gfile_min,gfile_max) = findMinMax(gfile_list)
        print gfilefile," ",gfile_min," ",gfile_max
        translate(gfile_list,[gfile_y-gfile_min[0],
                            gfile_x-gfile_min[1],
                            locationz],
                            verbose,True)
        mergelist.append(gfile_list)


    
    
    output_cmd_list=[]
    #write first files startup code to file dumps the rest of the startup codes
    for cmd in mergelist[0][0].cmds:
        output_cmd_list.append(cmd)
        
    for cmd_group in mergelist:
        cmd_group.pop(0)
    
    newlist = []
    for file in mergelist:
        for layer in file:
            newlist.append(layer)
            #print layer.z
    newlist.sort(key=lambda x: x.stackz)
    

    
    
    previous_layer_type = 0
    
    for cmd_layer in newlist:
        if clearance:
            rc = RaiseCmd%(clearance,zspeed)
            z_shift = cmd_layer.cmds.pop(0)
            xy = cmd_layer.cmds.pop(0)
            
            output_cmd_list.append(rc)
            output_cmd_list.append(xy)
            output_cmd_list.append(z_shift)
            output_cmd_list.append(xy)
        for cmd in cmd_layer.cmds:
            output_cmd_list.append(cmd)
    
    

    
    outfile = open(outfilename, 'w')
    for line in output_cmd_list:
        pass
        outfile.write(line)
   
    
    print "done"
    
    

if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    sys.exit('usage: test.py <xmlfile> <outputfile> [--verbose]')
    infilename = XMLFile#sys.argv[1]
    outfilename = OutFile#sys.argv[2]
    mergeFromXML(infilename,outfilename,'--verbose' in sys.argv, '--debug' in sys.argv )
    
 