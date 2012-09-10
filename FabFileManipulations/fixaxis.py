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
            for ytag in point.findall("y"):
                y = float(ytag.text)
                y = -y
                ytag.text = "%f" % y
    
    print "woot"
    indent(root)
    fabTree.write(sys.argv[2])
    
    
