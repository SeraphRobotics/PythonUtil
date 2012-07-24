#!/usr/bin/env python

import xml.etree.ElementTree as etree
import xml, sys, copy, os

"""
Sample Generating Tool: 

Script that generates either a single layer calibration .xdfl file (approx. 35mm x
 35 mm), used to measure the average path height of a material path, or generates a three-dimensional sample .xdfl file (approx. 35 x 35 x 35 mm). 

A single layer calibration file will be generated if the final command line argument
 (<path_height>) is omitted. Otherwise, the three-dimensional sample will be created

"""

def indent(elem, level=0):
	
	# Helper function that fixes the indentation scheme of a given Element object
	# and all of its subelements
	#
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

def createSkeleton(): 
	
	# Helper function that returns an ElementTree representation of a skeleton
	# .xdfl file, which consists of the xdfl wrapper elements, and empty palette
	# element and an empty commands element

	root = etree.Element("xdfl")
	root.append(etree.Element("palette"))
	root.append(etree.Element("commands"))
	tree = etree.ElementTree(root)
	
	return tree	

def initializePalette(tree, p_width, p_speed, p_height, c_vol, a_const):

	# Helper function that initializes the palette element of the calibration
	# file being generated, using the material properties given as arguments

	material = etree.SubElement(tree.find("palette"), "material")	
	etree.SubElement(material, "id").text = "1"
	etree.SubElement(material, "areaConstant").text = str(a_const)
	etree.SubElement(material, "compressionVolume").text = str(c_vol)
	etree.SubElement(material, "name").text = "material_1"
	etree.SubElement(material, "pathHeight").text = str(p_height)
	etree.SubElement(material, "pathSpeed").text = str(p_speed)
	etree.SubElement(material, "pathWidth").text = str(p_width)
	return material

def makePoint(x, y, z):

	point = etree.Element("point")
	etree.SubElement(point, "x").text = str(x)	
	etree.SubElement(point, "y").text = str(y)
	etree.SubElement(point, "z").text = str(z)
	
	return point

def writeTree(output_file, tree):

	f = open(output_file, 'w')
	f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?> \n")
	indent(tree.getroot())
	string = etree.tostring(tree.getroot())
	f.write(string)
	f.close()

def addLayer(tree, p_width, height, start_x, start_y, start_z, s):

	#Single layer path here (35mm)
	path = etree.SubElement(tree.find("commands"), "path")
	point_list = []
	coordinate_list = []
	point_list.append(makePoint(start_x, start_y - p_width, start_z + height))
	coordinate_list.append((start_x, start_y - p_width, start_z + height))
	length_count = s

	while length_count > 0.0: 
		last_point = point_list[-1]
		last_x = float(last_point.find("x").text)
		last_y = float(last_point.find("y").text)
		last_z = float(last_point.find("z").text)

		new_point = makePoint(last_x, last_y + p_width, last_z)
		point_list.append(new_point)
		coordinate_list.append((last_x, last_y + p_width, last_z))
		length_count -= p_width
	
		if last_x == 0.0:
			point_list.append(makePoint(last_x + s, last_y + p_width, last_z))	
			coordinate_list.append((last_x + s, last_y + p_width, last_z))
		
		else: 		
			point_list.append(makePoint(last_x - s, last_y + p_width, last_z))
			coordinate_list.append((last_x - s, last_y + p_width, last_z))

	path.extend(point_list[1:])
	return coordinate_list[1:]

def createTransition(start, end, clear, spd):
		
	# Helper function that returns a "non-material" transition path at speed
	# spd using a clearance of clear

	transition, speed = etree.Element("path"), etree.Element("speed")
	speed.text = str(spd)
	start, end  = copy.deepcopy(start), copy.deepcopy(end)
	clear_a, clear_b = copy.deepcopy(start), copy.deepcopy(end)	
	clear_a.find("z").text = str(float(start.find("z").text) + clear)
	clear_b.find("z").text = str(float(end.find("z").text) + clear)
	transition.extend([speed, start, clear_a, clear_b, end])
	return transition


def generateCalibrationLayer(out_f, s, p_width, p_speed, height, a_const, c_vol):

	# Helper function that generates an .xdfl file corresponding to a single
	# layer calibration print for the purposes of measuring average path height
	# for a given offset height "height". The output .xdfl file will be written to
	# "out_f".

	tree = createSkeleton()
	initializePalette(tree, p_width, p_speed, p_width, c_vol, a_const)
	addLayer(tree, p_width, height, 0.0, 0.0, 0.0, s) #Will change
	writeTree(out_f, tree)	

def pointsToPath(material, points):

	# Helper function that converts a list of coordinates (bundled in tuples)
	# into a list of Elements with the "point" tag

	path = etree.Element("path")
	material_id = etree.SubElement(path, "materialID")
	material_id.text = material.find("id").text

	for p in points:
		point = etree.SubElement(path, "point")
		x = etree.SubElement(point, "x")
		x.text = str(p[0])
		y = etree.SubElement(point, "y")
		y.text = str(p[1])
		z = etree.SubElement(point, "z")
		z.text = str(p[2])
	
	return path

def updateMetaData(p_width, p_height, p_speed, height, tip, q):

	if not os.path.isfile("METADATA.txt"):
		f = open("METADATA.txt", 'a+')
		f.write("Contents of each line are: path width, path height, path speed, offset height, tip, PSI, sample number \n")
		f.close() 

	f = open("METADATA.txt", 'r')
	lines = f.readlines()
	f.close()

	f = open("METADATA.txt", 'a+')
	sample_n = None
	if "Contents" in lines[-1]: sample_n = "1"
	else: sample_n = int(lines[-1].split(",")[-1]) + 1	
	out = [str(x) for x in [p_width, p_height, p_speed, height, tip, q, sample_n]]
	f.write(", ".join(out) + "\n")	
	f.close()

def generateSample(tip, out_f, s, p_width, p_speed, p_height, height, q, a_const,c_vol):

	# Helper function that generates both a .xdfl file corresponding to a multi-
	# layer (cube) calibration print, as well as a .csv metadata file containing 
	# the original arguments to the function for record purposes. The output .xdfl
	# file will be written to "out_f". If a .csv file already exists, use the 
	# existing one.

	tree = createSkeleton()
	material = initializePalette(tree, p_width, p_speed, p_height, c_vol, a_const)
	#last_layer = addLayer(tree, p_width, height, 0.0, 0.0, 0.0, s) 
	def_layer = addLayer(tree, p_width, height, 0.0, 0.0, 0.0, s)
	rot_layer = []
	
	for p in def_layer:
		rot_layer.append((-p[1] + s, p[0], p[2] + p_height)) 

	last_layer = def_layer

	height_count = s - p_height
	layer_count = 0
	commands = tree.find("commands")

	while height_count > 0.0:
		new_layer = []
		layer_type = def_layer
		if (layer_count & 1) == 0:
			layer_type = rot_layer

		for p in layer_type:
			new_layer.append((p[0], p[1], last_layer[0][2] + p_height)) 
		
		strt, lst = last_layer[-1], new_layer[0]
		start = makePoint(strt[0], strt[1], strt[2])
		end = makePoint(lst[0], lst[1], lst[2])
		commands.extend(createTransition(start, end, 2 * p_height, p_speed))
		commands.extend(pointsToPath(material, new_layer)) 
			
		last_layer = new_layer
		layer_count += 1
		height_count -= p_height

	writeTree(out_f, tree)
	updateMetaData(p_width, p_height, p_speed, height, tip, q)

if __name__ == "__main__":

	if len(sys.argv) < 9:
		print "Usage: python calibrate.py <output_file_path> <path_width> <path_speed> <Q (psi)> <offset_height> <area_constant> <compression_volume> <tip> [<path_height>] \n (Arguments in brackets are optional)"
		sys.exit(0)

	out_file, p_width, p_speed = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
	q,h,a_c = float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
	c_v, t =  float(sys.argv[7]), float(sys.argv[8])

	if len(sys.argv) > 9:
		p_height = float(sys.argv[9])
		generateSample(t,out_file, 35.0, p_width, p_speed, p_height, h, q, a_c, c_v)

	else: generateCalibrationLayer(out_file, 35.0, p_width, p_speed, h, a_c, c_v)
		
		
