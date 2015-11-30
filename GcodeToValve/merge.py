#!/usr/bin/env python

import math
import os
import re
import sys
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree




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
        else: newlayer.stackz+=10;
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
    
def setTopcoatSpeed(layerlist,xyspeed, verbose=False):
     for layer in layerlist :
        out_line_list=[]
        previous=[0]*4
        for line in layer.cmds:
            topcoat_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) Z([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                             line.rstrip())
            if topcoat_match:
                if verbose: print "extrude: ", topcoat_match.groups()
                p2 =[0]*4
                delta=[0]*3
                
                for j in range(0,4):
                    group = topcoat_match.groups()[j]
                    if not (type(group)==type(None)):
                        if "f" in group.lower():
                            p2[3]=topcoat_match.groups()[j+1]
                            break
                        else:
                            p2[j]=float(group)
                speed=""
                if (previous[0]==0 and previous[1]==0):
                    if p2[3]>0:
                        speed = " F%f"%float(p2[3])
                else:
                    delta[0] = p2[0]-previous[0]
                    delta[1] = p2[1]-previous[1]
                    delta[2] = p2[2]-previous[2]
                    dxyz = math.sqrt(delta[0]*delta[0]+delta[1]*delta[1]+delta[2]*delta[2])
                    dxy = math.sqrt(delta[0]*delta[0]+delta[1]*delta[1])
                    dz = math.sqrt(delta[2]*delta[2])
                    f=0
                    if dxyz: f = xyspeed*1+600*dz/dxyz #dxy/dxyz+1200*dz/dxyz
                    else: f=xyspeed
                    #print dxyz,dxy,f
                    speed = " F%f"%f
                    
                previous = p2
                

                newline = "G1 X%f Y%f Z%f%s\n"%(p2[0],p2[1],p2[2],speed)
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
    
    BUILDTRAY_OFFSET = [20,34,19.75]
    TOOLHEAD_OFFSET  = [-10,63,-4.5]
    
    if debug:
        BUILDTRAY_OFFSET = [0,0,0]
        TOOLHEAD_OFFSET  = [0,0,0]
    
    lowercmds="G4 P2\nM340 P1 S600\nG4 P1000\nM340 P1 S0\n"
    raisecmds="G4 P2\nM340 P1 S1200\nG4 P1000\nM340 P1 S0\n"
    
    
    def nodeToFileOffset(node):
        file = node.find("file").text
        zoffset = float(node.find("zoffset").text)
        ztranslate = float(node.find("ztranslate").text)
        xcenter= float(node.find("xcenter").text)
        ycenter = float(node.find("ycenter").text)
        return [file,zoffset,ztranslate,xcenter,ycenter]
    
    ## Process file 
    root = fabTree.getroot()
    shellnode = root.find("shell")
    padnodes = root.findall("pad")
    topcoatnode = root.find("topcoat")
    

    
    ## make shell layer list
    [shellfile,zshell_offset,zshell,xshell,yshell] = nodeToFileOffset(shellnode)
    shell_list = processFileIntoLayers(shellfile,True,verbose)
    parity(shell_list,verbose)
    (shell_min,shell_max) = findMinMax(shell_list)
    if debug:
        print "shell"
        print findMinMax(shell_list)
        
        

    translate(shell_list,[-shell_min[0]+BUILDTRAY_OFFSET[0],-shell_min[1]+BUILDTRAY_OFFSET[1],zshell+BUILDTRAY_OFFSET[2]],verbose)
    #translate(shell_list,BUILDTRAY_OFFSET,verbose)
    mergelist = []
    mergelist.append(shell_list)
    
    ## make Pad layer lists
    
    for padnode in padnodes:
        [padfile,padz,locationz,pad_x,pad_y] = nodeToFileOffset(padnode)
        pad_list = processFileIntoLayers(padfile,False,verbose)
        parity(pad_list,verbose)
        (pad_min,pad_max) = findMinMax(pad_list)
        if debug:
            print "pads"
            print findMinMax(pad_list)
        translate(pad_list,[pad_y-pad_min[0]+TOOLHEAD_OFFSET[0]+BUILDTRAY_OFFSET[0],
                            pad_x*2-pad_min[1]+TOOLHEAD_OFFSET[1]+BUILDTRAY_OFFSET[1],
                            locationz+TOOLHEAD_OFFSET[2]+padz+BUILDTRAY_OFFSET[1]],
                            verbose,True)
        #translate(pad_list,[TOOLHEAD_OFFSET[0],TOOLHEAD_OFFSET[1],TOOLHEAD_OFFSET[2]+padz],verbose)
        #translate(pad_list,BUILDTRAY_OFFSET,verbose)
        mergelist.append(pad_list)
    
    ## make TopCoat layer lists
    [topcoat_file,z_topcoat,z_offset,x_offset,y_offset] = nodeToFileOffset(topcoatnode)
    topcoat_list = processFileIntoLayers(topcoat_file,True,verbose)
    parity(topcoat_list,verbose)
    (topcoat_min,topcoat_max) = findMinMax(topcoat_list)
    translate(topcoat_list,[-topcoat_min[0]+TOOLHEAD_OFFSET[0]+x_offset+BUILDTRAY_OFFSET[0],
                            -topcoat_min[1]+TOOLHEAD_OFFSET[1]+y_offset,
                            z_topcoat+z_offset+TOOLHEAD_OFFSET[2]+BUILDTRAY_OFFSET[2]],
                            verbose, True)
    #translate(topcoat_list,[TOOLHEAD_OFFSET[0]+x_offset,TOOLHEAD_OFFSET[1]+y_offset,TOOLHEAD_OFFSET[2]+z_offset],verbose)
    #translate(topcoat_list,[BUILDTRAY_OFFSET[0],BUILDTRAY_OFFSET[1],BUILDTRAY_OFFSET[2]],verbose)
    #setTopcoatSpeed(topcoat_list,1200,verbose)

    
    
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
        if (previous_layer_type != cmd_layer.type):
            if (previous_layer_type != Layer.displacement):
                output_cmd_list.append(lowercmds)
#                print "lower"
            elif (previous_layer_type == Layer.displacement):
#                print "Raise"
                output_cmd_list.append(raisecmds)
            else:
#                print "type: %i"%cmd_layer.type
                output_cmd_list.append(raisecmds)
        
#        print "layer type: %i"%cmd_layer.type
        previous_layer_type = cmd_layer.type
        for cmd in cmd_layer.cmds:
            output_cmd_list.append(cmd)
    
    

    
    outfile = open(outfilename, 'w')
    for line in output_cmd_list:
        pass
        outfile.write(line)
    
    
    for layer in topcoat_list:
        for cmd in layer.cmds:
            outfile.write(cmd)
    
    print "done"
    
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: test.py <xmlfile> <outputfile> [--verbose]')
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    mergeFromXML(infilename,outfilename,'--verbose' in sys.argv, '--debug' in sys.argv )
    
 