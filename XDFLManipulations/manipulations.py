########################Imports####################################################
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree
from math import cos, sin, pi


######################## Global Defs ################################################
axes = ["x", "y", "z"]
DEBUG = False
######################## Helper Functions ###########################################



def pointsListFromPathEl(pathEl):
    pointsList=[]
    for pointEl in pathEl.iter("point"):
        pList = pointListFromPointEl(pointEl)
        pointsList.append(pList)
    return pointsList

def pointListFromPointEl(pointEl):
    indecies = [0,1,2]
    pList=[0,0,0]
    for index in indecies:
        el = pointEl.find(axes[index])
        val = float(el.text)
        pList[index]=val
    return pList

def pathFromPointsList(pointsList, id=0, speed=10):
    p = Element("path")
    
    ## if id is given, make it a materialID path, else add a speed tag
    if(id>0):
        matIdEl = Element("materialid")
        matIdEl.text = "%i"%id
        p.append(matIdEl)
    else:
        speedEl = Element("speed")
        speedEl.text="%f"%speed
        p.append(speedEl)
    
    ###Add Points of the form [[x1,y1,z1],[x2,y2,z2],...]
    for pointList in pointsList:
        pointEl = pointFromList(pointList)
        p.append(pointEl)
    return p

def pointFromList(pointAsList):
    ### Take a point [x,y,z] to XDFL format
    indecies = [0,1,2]
    p = Element("point")
    for index in indecies:
        el = Element(axes[index])
        el.text = "%f"%pointAsList[index]
        p.append(el)
    return p

##########################GLOBAL MANIPULATIONS ####################################
def sortIntoLayers(fabTree):
    slices={}
    root = fabTree.getroot()
    cmd = root.find("commands")
    for path in cmd.iter("path"):
        z = float(path.find("point").find("z").text)
        if z in slices.keys(): slices[z].append(path)
        else: slices[z]=[path]
        cmd.remove(path)

    for z in sorted(slices.keys()):
        for path in slices[z]:
            cmd.append(path)
    return fabTree

def threshold(fabTree, threshold=0):
    "This will threshold a fabFile element tree and return the tree"
    for path in fabTree.iter("path"):
        zValue = float(path.find("point").find("z").text)
        if zValue <= threshold: fabTree.getroot().remove(path)
    return fabTree
    
def dimensions(fabTree, name=None):
    minvalues = [0, 0, 0]
    maxvalues = [0, 0,0]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.iter("path"):
        for point in path.findall("point"):
            for i in range(0, 3):
                el = point.find(axes[i])
                if(type(None)==type(el)):
                    if(DEBUG): print "no", axes[i]
                    pass
                else:
                    val = float(el.text)
                    if (val > maxvalues[i]): maxvalues[i]=val
                    if (val < minvalues[i]): minvalues[i]=val
            
            
    return (minvalues,maxvalues)

def startpath(fabTree, number):
    root = fabTree.getroot()
    cmd = root.find("commands")
    i = 0;
    for path in fabTree.iter("path"):
        i= i+1
        if (i < number):
            if(DEBUG): print "removed ",i 
            cmd.remove(path)
    return fabTree
    
def dropClearance(fabTree):
    root = fabTree.getroot()
    cmd = root.find("commands")
    i = 0;
    for path in fabTree.iter("path"):
        matid=0
        matidel = path.find("materialID")
        if (type(None) == type(matidel)): 
            matidel = path.find("materialid")
        if (type(None) != type(matidel)): 
            matid = int(matidel.text)
        if (matid==0):
            cmd.remove(path)
    return fabTree    
    
def setClearance(fabTree, clearance, speed= 10):
        ### ONLY WORKS FOR PATH ONLY COMMANDS! Will drop Dwell or Voxel tags
        # remove old clearances
        fabTree = dropClearance(fabTree)
        
        
        root = fabTree.getroot()
        oldcmd = root.find("commands")
        newcmd = Element("commands")
        
        firstpath=True
        lastpoint=[0,0,0]
        for path in oldcmd.iter("path"):
            ##Turn path into points list
            pathpoints = pointsListFromPathEl(path)
            if (not len(pathpoints)):
                if(DEBUG): print "missing points in path"
                continue
            
            if firstpath:
                # if first path, do nothing
                firstpath = False;
            else:
                ##Get Last Point from last path
                #lastpoint
                ##Get first point from this path
                firstpoint = pathpoints[0]
                ##make clearance path between
                pointA = [lastpoint[0],lastpoint[1],lastpoint[2]+clearance]
                pointB = [firstpoint[0],firstpoint[1],firstpoint[2]+clearance]
                pointslist=[lastpoint,pointA,pointB,firstpoint]
                transitionpath = pathFromPointsList(pointslist,0,speed)
                newcmd.append(transitionpath)
            
            ## add path to new commands and set last point
            newcmd.append(path)
            lastpoint = pathpoints[-1]
        root.remove(oldcmd)
        root.append(newcmd)
        return fabTree

def xdfl2fab(fabTree):
    ### NEED TO TRANSFORM MATERIALS############
    newroot = Element("fabAtHomePrinter")
    newTree = ElementTree(newroot)
    pathaccel = Element("printAcceleration")
    newroot.append(pathaccel)
    pathaccel.text = "100"
    matcal = Element("materialCalibration")
    newroot.append(matcal)
    for path in fabTree.iter("path"):
        if not(len(path.findall("speed"))):
            newroot.append(path)
    return newTree
    
##################MANIPULATIONS ON EACH POINT (OR MATERIAL'S POINTS)###############################
def forEachPoint(fabTree, argFunction, arguments, targetMatId=-1):
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.iter("path"):
        matid=0
        matidel = path.find("materialID")
        if (type(None) == type(matidel)): 
            matidel = path.find("materialid")
        if (type(None) != type(matidel)): 
            matid = int(matidel.text)
        
        if(DEBUG):print "ID is %i, target is%i"%(matid,targetMatId)
        
        if ((targetMatId==-1) or (matid== targetMatId)):
            if(DEBUG):print "doing"
            for point in path.findall("point"):
                elements = []
                for i in range(0,3):elements.append(Element(axes[i]))
                values = [0, 0, 0]
                for i in range(0, 3):
                    el = point.find(axes[i])
                    if(type(None)==type(el)):
                        if(DEBUG):print "no", axes[i]
                        pass
                    else:
                        elements[i] = el
                        val = float(el.text)
                        values[i]=val
                newvalues = argFunction(values,arguments)
                for i in range(0,3):
                    elements[i].text = "%f"%newvalues[i]
    return fabTree

def scale(fabtree, dx=0, dy=0, dz=0, mid=-1):
    "This will scale element tree and return the tree"
    def scaler(pointvalues, arguments):
        newvalues=[]
        for i in range(0,3): newvalues.append(pointvalues[i]*arguments[i])
        return newvalues     

    values = [dx, dy, dz]
    return forEachPoint(fabTree, scaler, values, mid) 
    
def translate(fabTree, dx=0, dy=0, dz=0,id=-1):
    "This will translate a element tree and return the tree"
    def translator(pointvalues,arguments):
        newvalues=[]
        for i in range(0,3): newvalues.append(pointvalues[i]+arguments[i])
        return newvalues
    
    values = [dx, dy, dz]    
    return forEachPoint(fabTree, translator, values, id) 

def rotate(fabTree, theta,axis='z',id=-1):
    "This will rotate element tree and return the tree"
    def rotatorZ(values,arguments):
        thetaInRadians=arguments[0]/180*pi
        newvalues=[0,0,0]
        newvalues[0] = cos(thetaInRadians)*values[0]-sin(thetaInRadians)*values[1]
        newvalues[1] = sin(thetaInRadians)*values[0]+cos(thetaInRadians)*values[1]   
        newvalues[2] = values[2]
        return newvalues
    
    def rotatorY(values,arguments):
        thetaInRadians=arguments[0]/180*pi
        newvalues=[0,0,0]
        newvalues[0] = cos(thetaInRadians)*values[0]-sin(thetaInRadians)*values[2]
        newvalues[1] = values[1]   
        newvalues[2] = sin(thetaInRadians)*values[0]+cos(thetaInRadians)*values[2]
        return newvalues    
    
    def rotatorX(values,arguments):
        thetaInRadians=arguments[0]/180*pi
        newvalues=[0,0,0]
        newvalues[0] = values[0]
        newvalues[1] = cos(thetaInRadians)*values[1]-sin(thetaInRadians)*values[2]   
        newvalues[2] = sin(thetaInRadians)*values[1]+cos(thetaInRadians)*values[2]
        return newvalues        
    
    axis.lower()
    if(axis=='x'):
        return forEachPoint(fabTree, rotatorX, [theta], id) 
    elif(axis=='y'):
        return forEachPoint(fabTree, rotatorY, [theta], id) 
    elif(axis=='z'):
        return forEachPoint(fabTree, rotatorZ, [theta], id)     
        
        
def parity(fabTree, id=-1):
    "This will parity transform the points in the XY plane of a element tree and return the tree"
    def parityor(values,arguments):
        newvalues=[0,0,0]
        newvalues[0] = values[1]
        newvalues[1] = values[0]
        newvalues[2] = values[2]
        return newvalues
    
    return forEachPoint(fabTree,parityor,[],id)

def mirror(fabTree, axisname, id=-1):
    
    def glass(values,arguments):
        axisname = arguments[0]
        axisname.lower()
        
        axes = ["x","y","z"]
        signs=[1,1,1]
        newvalues=[0,0,0]
        
        for i in range(0,len(axes)):
            signs[i] = 2*int(not(axisname==axes[i]))-1
        for i in range(0,len(values)):
            newvalues[i] = signs[i]*values[i]
        
        return newvalues
        
    return forEachPoint(fabTree,glass,[axisname],id)
    
#####################################################
def indent(elem, level=0):
    # Helper function that fixes the indentation scheme of a given Element object and all of its subelements
    # Modified from: http://infix.se/2007/02/06/gentlemen-indent-your-xml
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def writeTree(output_file, tree):
    f = open(output_file, 'w')
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?> \n")
    indent(tree.getroot())
    string = etree.tostring(tree.getroot())
    f.write(string)
    f.close()    
    
if __name__ == '__main__':
    import sys

    if(len (sys.argv)<2 ):
        todo = "help"
    else:
        todo = sys.argv[1]
    
    todo=""
    if (len(sys.argv)>2):
        todo = sys.argv[1]
    else:
        todo = "help"

    
    def print_error():
        print "Incorrect number of arguments, try help"
        print todo
        print sys.argv
    
    if todo== "help":
        print " theshold\tmanipulations.py threshold 'file name' ('write name')"
        print " translate\tmanipulations.py translate 'file name' x y z (id)"
        print " rotate  \tmanipulations.py rotate 'file name' theta axis('write name')"
        print " parity  \tmanipulations.py parity 'file name' ('write name')"
        print " mirror  \tmanipulations.py mirror 'file name' 'axis' ('write name')"
        print " startpath\tmanipulations.py startpath 'file name' index ('write name')"
        print " dimensions\tmanipulations.py dimensions 'file name' "
        print " drop clearance\tmanipulations.py dropclearance 'filename' ('write name')"
        print " set clearance\tmanipulations.py setclearance 'filename' clearance (speed)"
        print " scale  \tmanipulations.py scale 'filename' x y z ('write name')"
        print " toFab  \tmanipulations.py toFab 'filename' ('write name')"
        
    else: 
        fabTree = ElementTree(file = sys.argv[2])
        for el in fabTree.iter(): el.tag = el.tag.lower()
    
        if todo == "threshold":
            #threshold fabFile NewFab
            fabTree = threshold(fabTree)
            if len(sys.argv)>3:writeTree(sys.argv[3], fabTree)
            else:writeTree(sys.argv[2],fabTree)
            
        elif todo == "translate":
            #translate fabfile x yz
            if len(sys.argv)>5:
                x = float(sys.argv[3])
                y = float(sys.argv[4])
                z = float(sys.argv[5])
                id=-1
                if len(sys.argv)>6:
                    id = int(sys.argv[6])
                fabTree=translate(fabTree, x, y, z, id)
                writeTree(sys.argv[2], fabTree)    
            else: print_error()
        
        elif todo == "rotate":
            if len(sys.argv)>2:
                theta = float(sys.argv[3])
                axis = sys.argv[4]
                fabTree=rotate(fabTree,theta,axis)
                if len(sys.argv)>5: writeTree(sys.argv[5], fabTree)
                else: writeTree(sys.argv[2], fabTree)                
            else: print_error()

        elif todo == "parity":
            fabTree=parity(fabTree)
            if len(sys.argv)>3: writeTree(sys.argv[3],fabTree)
            else: writeTree(sys.argv[2],fabTree)
        
        elif todo == "mirror": 
            print "len sys.argv ", sys.argv
            fabTree=mirror(fabTree, sys.argv[3])
            if len(sys.argv)>4: writeTree(sys.argv[4],fabTree)
            else: writeTree(sys.argv[2],fabTree)
            print "done"            
        elif todo == "dimensions":
            (minvalues,maxvalues) = dimensions(fabTree)
            print minvalues,maxvalues

        elif todo == "startpath":
            number = float(sys.argv[3])
            fabTree=startpath(fabTree,number)
            if len(sys.argv)>4: writeTree(sys.argv[4],fabTree)
            else: writeTree(sys.argv[2],fabTree)
            
        elif todo == "dropclearance":
            fabTree=dropClearance(fabTree)
            if len(sys.argv)>3: writeTree(sys.argv[3],fabTree)
            else: writeTree(sys.argv[2],fabTree)
            
        elif todo == "setclearance":
            clearance = float(sys.argv[3])
            speed = 10
            if len(sys.argv)>4: speed = float(sys.argv[4])
            fabTree=setClearance(fabTree,clearance,speed)
            writeTree(sys.argv[2],fabTree)
            
        elif todo == "scale":
            if len(sys.argv)>6:
                x = float(sys.argv[3])
                y = float(sys.argv[4])
                z = float(sys.argv[5])
                fabTree=scale(fabTree, x, y, z)
                writeTree(sys.argv[6], fabTree)    
            else: print_error()
            
        elif todo == "toFab":
            fabTree=xdfl2fab(fabTree)
            writeTree(sys.argv[3], fabTree)    
