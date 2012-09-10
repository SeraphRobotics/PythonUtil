from xml.etree.ElementTree import ElementTree 

def fix(fabTree):
    axes = ["x", "y", "z"]
    "This will translate a fabFile element tree and return the tree"
    for path in fabTree.getiterator("path"):
        for point in path.findall("point"):
            el = point.find("z")
            val = -float(el.text)
            el.text = "%f"%val
    return fabTree
    
    
if __name__ == '__main__':
    import sys
    print"starting"
    fabTree = ElementTree(file = sys.argv[1])
    print "loaded"
    fabTree = fix(fabTree)
    print "fixed"
    fabTree.write("new.fab")
    print "written"
