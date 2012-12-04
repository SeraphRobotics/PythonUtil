
from xml.etree.ElementTree import ElementTree, Element 
from math import cos, sin, pi

##########################GLOBAL MANIPULATIONS ####################################
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
    
def dropClearance(fabTree):
    root = fabTree.getroot()
    cmd = root.find("commands")
    i = 0;
    for path in fabTree.getiterator("path"):
        matid=0
        matidel = path.find("materialID")
        if (type(None) == type(matidel)): 
            matidel = path.find("materialid")
        if (type(None) != type(matidel)): 
            matid = int(matidel.text)
        if (matid==0):
            cmd.remove(path)
    return fabTree    
    
    
    
    
##################MANIPULATIONS ON EACH POINT (OR MATERIAL'S POINTS)###############################
def forEachPoint(fabTree, argFunction, arguments, targetMatId=-1):
    axes = ["x", "y", "z"]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        matid=0
        matidel = path.find("materialID")
        if (type(None) == type(matidel)): 
            matidel = path.find("materialid")
        if (type(None) != type(matidel)): 
            matid = int(matidel.text)
        
        print "ID is %i, target is%i"%(matid,targetMatId)
        
        if ((targetMatId==-1) or (matid== targetMatId)):
            print "doing"
            for point in path.findall("point"):
                elements = []
                for i in range(0,3):elements.append(Element(axes[i]))
                values = [0, 0, 0]
                for i in range(0, 3):
                    el = point.find(axes[i])
                    if(type(None)==type(el)):
                        print "no", axes[i]
                    else:
                        elements[i] = el
                        val = float(el.text)
                        values[i]=val
                newvalues = argFunction(values,arguments)
                for i in range(0,3):
                    elements[i].text = "%f"%newvalues[i]
    return fabTree

def translator(values,arguments):
    newvalues=[]
    for i in range(0,3): newvalues.append(values[i]+arguments[i])
    return newvalues
    
def translate(fabTree, dx=0, dy=0, dz=0,id=-1):
    values = [dx, dy, dz]
    "This will translate a fabFile element tree and return the tree"
    return forEachPoint(fabTree, translator, values, id) 

def rotator(values,arguments):
    thetaInRadians=arguments[0]/180*pi
    newvalues=[0,0,0]
    newvalues[0] = cos(thetaInRadians)*values[0]-sin(thetaInRadians)*values[1]
    newvalues[1] = sin(thetaInRadians)*values[0]+cos(thetaInRadians)*values[1]   
    newvalues[2] = values[2]
    return newvalues

def rotate(fabTree, theta,id=-1):
    "This will translate a fabFile element tree and return the tree"
    return forEachPoint(fabTree, rotator, [theta], id) 
    
    
def parityor(values,arguments):
    newvalues=[0,0,0]
    newvalues[0] = values[1]
    newvalues[1] = values[0]
    newvalues[2] = values[2]
    return newvalues
    
def parity(fabTree, id=-1):
    return forEachPoint(fabTree,parityor,[],id)
    




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
            id=-1
            if len(sys.argv)>6:
                id = int(sys.argv[6])
            fabTree=translate(fabTree, x, y, z, id)
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

    elif todo == "startpath":
        number = float(sys.argv[3])
        fabTree=startpath(fabTree,number)
        fabTree.write(sys.argv[2])
        
    elif todo == "dropclearance":
        fabTree=dropClearance(fabTree)
        fabTree.write(sys.argv[2])    

