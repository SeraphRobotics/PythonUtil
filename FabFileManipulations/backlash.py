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

from xml.etree.ElementTree import ElementTree , Element
from math import sqrt,  pow

def sign(number):
    """Will return 1 for positive,
    -1 for negative, and 0 for 0"""
    try:return number/abs(number)
    except ZeroDivisionError:return 0

    
    
def compensateFabTree(fabTree,bx, by, bz):
    """
    http://www.xml.com/pub/a/2003/02/12/py-xml.html
    http://docs.python.org/library/xml.etree.elementtree.html
    """
    
        
    b = [bx, by, bz]
    signs = [0, 0, 0]
    last_point = [0,0, 0]   
    delta = [0, 0, 0]
    
    
    root = fabTree.getroot()
    for element in root.getiterator("path"): ## getiterator = iter in 2.7 on
        for elpoint in element.findall("point"):
            point = Point(elpoint)
            current = [point.getX(), point.getY(), point.getZ()]
            
            for i in range(0, 3):
                current_sign = sign(current[i]-last_point[i])
                if (current_sign > signs[i]): delta[i]=b[i]
                if (current_sign< signs[i]): delta[i]=-b[i]
                signs[i]=current_sign

            last_point = current
            elx = elpoint.find("x")
            elx.text = "%f"%(current[0]+delta[0])
            ely = elpoint.find("y")
            ely.text = "%f"%(current[1]+delta[1]) 
            elz = elpoint.find("z")
            elz.text = "%f"%(current[2]+delta[2])            
            
            
        return fabTree

    
if __name__ == "__main__":
    import sys
    if sys.argv[1]=="help":
        print "\n backlash.py 'fabfile' ('write name')"
    else:fabfile = sys.argv[1]
    
    if 2<len(sys.argv):  write_to_file = sys.argv[2]
    else: write_to_file = fabfile
    
    fabTree = ElementTree(file = fabfile )
    fabTree =  compensateFabTree(fabTree,1.0,  1.0, 1.0)
    
    fabTree.write(write_to_file)
    

    
    
    
