import xml.etree.ElementTree as etree
import xml,sys,copy,os
		
""" 
 .xdfl file merger:															
																				
Takes in several .xdfl files as command line arguments, and does the following: 

1. Merge the "palette" elements of all input files such that materials are
   sequentially and such that there are no duplicate materials

2. Merge the "commands" elements of all input files such that all paths can be 
   printed in one job

3. Link the paths with "non-material" transition paths when necessary

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

def MergeElements(trees): 

	# Helper function that merges the palette elements of the input .xdfl files,
	# as well as updates the references to the materials in the command elements of
	# the input files. 
	#
	# Input: 
	#	trees: A list of ElementTree objects representing each .xdfl file
	#
	# Output: 
	#	output: An ElementTree object representing the .xdfl with palettes merged
	#	output_commands: An Element representing the commands element of the output
	#   new_paths: A list of paths sorted by layer with no transition paths

	output = copy.deepcopy(trees[0]) #The element tree that will be the output
	output_palette = output.find("palette")
	output_commands = output.find("commands")
	material_index = {} #Maps Material properties tuple -> global material ID
	new_paths = []
	mat_spds = {}
	id_count = 0

	#Cleanup the output element tree
	while list(output_palette): output_palette.remove(list(output_palette)[0])
	#Remove paths from output element tree
	while list(output_commands): output_commands.remove(list(output_commands)[0])
			
	#Merge the palette elements of the given files into one palette element
	for t in trees: 
		p = t.find("palette")
		local_index = {}

		if not p is None:
			#Iterate through the materials in this palette. If a new material
			#is encountered, assign it a new id in the material_index
			for mat in list(p): 
				temp = tuple([x.text for x in list(mat) if x.tag != "id"])	
				old_index = mat.find("id").text

				if not temp in material_index:
					id_element = mat.find("id")
					id_count += 1
					id_element.text = str(id_count)
					material_index[temp] = id_count
					output_palette.append(mat)

					#Populate the material speeds dictionary
					if not int(id_count) in mat_spds:
						mat_spds[int(id_count)] = float(mat.find("pathspeed").text)
				local_index[old_index] = material_index[temp]

		#Iterate over all paths in the .xdfl, updating material references
		#Strip out paths that do not use a material
		com = t.find("commands")
		paths = com.findall("path")	

		for p in paths:
			if not p.find("materialid") is None:
				#to_add = copy.deepcopy(p)
				material_id = p.find("materialid")
				material_id.text = str(local_index[material_id.text])
				new_paths.append(p)

	#Sort the new paths by z-coordinate
	new_paths.sort(key = lambda path : float(path.find("point").find("z").text))
	return output, output_commands, new_paths, mat_spds

def LinkPaths(material_speeds, paths, clear):

	# Helper function that inserts  "non-material" transition paths between
	# material paths in a layer-sorted list of paths. 
	#
	# Input: 
	#	material_speeds: a map from material ids to their speeds
	#   paths: a list of layer-sorted path elements 
	#	clear: vertical clearance used in the transition paths
	#
	# Output:
	#  A list of paths with transition paths inserted

	def CreateTransition(start, end, clear, spd):
		
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

	new_paths = []
	#Create a transition from the default location to the first point 	
	start = copy.deepcopy(paths[0].find("point"))
	end = copy.deepcopy(paths[0].find("point"))
	start.find("x").text = "0.000000"
	start.find("y").text = "0.000000"
	start.find("z").text = "0.000000"
	new_paths.append(CreateTransition(start, end, clear, 30))
	new_paths.append(paths[0])

	for i in range(len(paths))[1:]:	
		last_material = new_paths[-1].find("materialid").text
		#The last point of the last path added to the new list
		start = new_paths[-1].findall("point")[-1]
		#The first point of the current path to-add
		end = paths[i].find("point") 
		speed = material_speeds[int(last_material)]

		if last_material == paths[i].find("materialid").text:
			#Merge this path onto the last path if the paths touch	
			x1, y1, z1 = float(start.find("x").text), float(start.find("y").text),                              float(start.find("z").text)	
		
			x2, y2, z2 = float(end.find("x").text), float(end.find("y").text),                          float(end.find("z").text)	
			
			if x1 == x2 and y1 == y2 and z1 == z2:
				start.extend(end.findall("point"))
			else: 
				new_paths.append(CreateTransition(start,end, clear, speed))
				new_paths.append(paths[i])	
		else: 
		 	new_paths.append(CreateTransition(start, end, clear, speed))	
			new_paths.append(paths[i])
			 
	return new_paths

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print """Usage: python merge.py <output_file> [<clearance>] <file1> <file2> ... <file n>
    	   (Arguments in brackets are optional)"""
		sys.exit(0)

	output_file = sys.argv[1]

	#Initialize ElementTrees for each input .xdfl  
	files = sys.argv[2:]
	clearance = 0.0

	if not os.path.isfile(files[0]):	
		clearance = float(files[0])
		files.remove(files[0])

	trees = [etree.ElementTree() for x in files]

	for i in zip(trees,files): i[0].parse(i[1])

	#Convert the contents of the trees to lowercase
	for t in trees:
		for el in t.iter(): el.tag = el.tag.lower()

	output, output_commands, paths, material_speeds  = MergeElements(trees)

	#Path connecting
	new_paths = LinkPaths(material_speeds, paths, clearance)
	output_commands.extend(new_paths)	
	indent(output.getroot())

	f = open(output_file, 'w')
	f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?> \n")
	string = etree.tostring(output.getroot())
	f.write(string)
	f.close()

