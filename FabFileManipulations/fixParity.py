'''
 Copyright (c) 2011, Jeffrey Lipton (jeffreyilipton@gmail.com) all rights reserved
 '''
from xml.etree.ElementTree import ElementTree,  Element
from math import floor, sqrt,  pow

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

if __name__ == "__main__":
    import sys
    fabTree = ElementTree(file = sys.argv[1])
    
    root = fabTree.getroot()
    for pathtag in root.findall("path"):
        for point in pathtag.findall("point"):
            xEl=point.find('x')
            yEl=point.find('y')
            x = float(xEl.text)
            y = float(yEl.text)
            yp = -x
            xp = y
            
            yEl.text= "%f" % yp
            xEl.text = "%f"%xp
            
    print "woot"
    indent(root)
    name = sys.argv[1]
    name.replace('.fab', '')
    name = name+'_partity.fab'
    fabTree.write(name)
    
    
