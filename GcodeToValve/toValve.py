#!/usr/bin/env python

import math
import os
import re
import sys

closeLine = "G4 P2\nM340 P0 S1650\n"
openLine = "G4 P2\nM340 P0 S2100\n"

class State:
    Moving = 1
    Extruding = 2

def setspeeds(inlist, outlist, xyspeed, zspeed, verbose=False):
    for line in inlist:
        xy_move_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
        z_move_match = re.match(r'^G1 Z([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
        extrude_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) E([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                         line.rstrip())
        if extrude_match and xyspeed>0:

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
            if p2[3]>0: speed = " F%f"%float(xyspeed)
            newline = "G1 X%f Y%f%s\n"%(p2[0],p2[1],speed)
            outlist.append(newline)
            
            
        elif xy_move_match and xyspeed>0:

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
                speed = " F%f"%xyspeed
            newline = "G1 X%f Y%f%s\n"%(m1[0],m1[1],speed)
            outlist.append(newline)
        elif z_move_match and zspeed>0:
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
            newline = "G1 Z%f F%f\n"%(z1[0],zspeed)
            outlist.append(newline)
        else:
            if verbose: print line
            outlist.append(line)
    
def translateToValvetool(infile, outlist, verbose=False):
    

    
    state = State.Moving
    
    
    for line in infile:
        xy_move_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
        z_move_match = re.match(r'^G1 Z([-\d\.]+)($| F)*([-\d\.]+)',line.rstrip())
        extrude_match = re.match(r'^G1 X([-\d\.]+) Y([-\d\.]+) E([-\d\.]+)($| F)*([-\d\.]+)',  ##$
                         line.rstrip())
        reset_match = re.match(r'^G92 E([-\d\.]+)',line.rstrip())
        retract_match = re.match(r'^G1 F([-\d\.]+) E([-\d\.]+)',line.rstrip())
        pre_extrude_match = re.match(r'^G1 E([-\d\.]+) F([-\d\.]+)',line.rstrip())
        
        tempchange_match = re.match(r'^M104 S([-\d\.]+)',line.rstrip())
        settemp_match = re.match(r'^M109 S([-\d\.]+)',line.rstrip())
        if extrude_match:

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
            if p2[3]>0: speed = " F%f"%float(p2[3])
            newline = "G1 X%f Y%f%s\n"%(p2[0],p2[1],speed)

            if state == State.Moving:
                outlist.append(openLine)
                state = State.Extruding
            outlist.append(newline)
            
            
        elif xy_move_match:

            if verbose: 
                print "move: ", xy_move_match.groups()
            if state == State.Extruding:
                outlist.append(closeLine)
                state = State.Moving

            
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
            newline = "G1 X%f Y%f%s\n"%(m1[0],m1[1],speed)
            outlist.append(newline)
        elif z_move_match:
            if verbose: print "Z_move: ", z_move_match.groups()
            if state == State.Extruding:
                outlist.append(closeLine)
                state = State.Moving

            z1 = [0]*2
            for j in range(0,2):
                group = z_move_match.groups()[j]
                if not (type(group)==type(None)):
                    if "f" in group.lower():
                        z1[1]=float(z_move_match.groups()[j+1])
                        break
                    else:
                        z1[j]=float(group)        

            newline = "G1 Z%f F%f\n"%(z1[0],z1[1])
            outlist.append(newline)
        elif reset_match:
            if verbose: print "reset"
        elif retract_match:
            if verbose: print "retract"
        elif pre_extrude_match:
            if verbose: print "pre-extrude"
        elif tempchange_match:
           if verbose:  print "set temp"
        elif settemp_match:
            if verbose:  print "temp"
        else:
            if verbose: print line
#            if state == State.Extruding:
                #outfile.write(closeLine)
                #state = State.Moving
            outlist.append(line)
    
    
            
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('usage: test.py <filename> <speed_xy> <speed_z> [--verbose]')
    infilename = sys.argv[1]
    speedx = sys.argv[2]
    speedz = sys.argv[3]
    
    
    outfilename = '%s.extrude%s' % os.path.splitext(infilename)
    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            outlist1=[]
            outlist2=[]
            translateToValvetool(infile, outlist1, '--verbose' in sys.argv)
            setspeeds(outlist1,outlist2,speedx,speedz, '--verbose' in sys.argv)
            outlist2.append(closeLine)
            for line in outlist2:
                outfile.write(line)
    
