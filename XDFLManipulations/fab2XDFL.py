########################Imports####################################################
from xml.etree.ElementTree import ElementTree, Element 
import xml.etree.ElementTree as etree
from math import cos, sin, pi


def processMaterials(root):
    nameIdDict = {}
    palette = Element("palette")
    
    i = 1
    for materialCal in root.iter("materialcalibration"):
        materialsElement = Element("material")

        nameEl = materialCal.find("name")
        materialsElement.append(nameEl)
        nameIdDict[nameEl.text] = i
        idtag = Element("id")
        idtag.text="%i"%i
        materialsElement.append(idtag)
        i+=1
        
        
        pwEl = materialCal.find("pathwidth")
        materialsElement.append(pwEl)
        
        phEl =Element("pathheight")
        phEl.text = pwEl.text
        materialsElement.append(phEl)
        
        psEl = materialCal.find("pathspeed")
        materialsElement.append(psEl)
        
        
        acEl = Element("areaconstant")
        acEl.text = "1"
        materialsElement.append(acEl)
        
        poEl = materialCal.find("pushout")
        po = float(poEl.text)
        cv = po*5000*0.000397
        cvEl = Element("compressionVolume")
        cvEl.text = '%.5f' % cv
        materialsElement.append(cvEl)
        palette.append(materialsElement)
        
    return nameIdDict,palette
        
def processPath(nameIdDict,oldPathEl):
    newPath = Element("path")
    matcalnameEl = oldPathEl.find("materialcalibrationname")
    id = nameIdDict[matcalnameEl.text]
    idtag = Element("materialID")
    idtag.text="%i"%id
    newPath.append(idtag)
    for pointEl in oldPathEl.iter("point"):
        newPath.append(pointEl)
    return newPath
    
        

def fab2XDFL(fabTree):
    newroot = Element("xdfl")
    newTree = ElementTree(newroot)

    cmds = Element("commands")
    
    nameIdDict,palette =  processMaterials(fabTree.getroot())
    
    for path in fabTree.iter("path"):
        if not(len(path.findall("speed"))):
            cmds.append(processPath(nameIdDict,path))
    newroot.append(palette)
    newroot.append(cmds)
    return newTree

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
        print "Incorrect number of arguments, try help"
        
    elif sys.argv[1]== "help":
        print " [fab file] {'write name')"

    else: 
        fabTree = ElementTree(file = sys.argv[1])
        for el in fabTree.iter(): el.tag = el.tag.lower()
        newTree = fab2XDFL(fabTree)
        outputname = sys.argv[1].replace(".fab","")
        outputname+=".xdfl"
        writeTree(outputname,newTree)
        print "Done"