import sys
import xml.etree.ElementTree as ET

infilename = ""
outfilename = ""
terrain_layer_name = ""
terrain_file_name = ""
terrain_tsx = ""
terrain_firstgid = 0

collision_layer_name = ""
collision_file_name = ""
collision_tsx = ""
collision_firstgid = 0

object_layer_name = ""
object_file_name = ""

collision_override_name = ""
override_file_name = ""

has_collision = False
has_objects = False
has_override = False

def usage():
	print("Usage:\nconv-tmx.py -in <in-file-name> -out <out-file-name> -terrain <terrain-layer-name> -terrainset <terrain tsx> (-collision <collision-layer-name> -collisionset <collision tsx> -objects <objects-layer-name> -override <override-layer-name>)")
	
def main():
	infilename = ""
	outfilename = ""
	
	terrain_layer_name = ""
	terrain_file_name = ""
	terrain_tsx = ""
	terrain_firstgid = 0

	collision_layer_name = ""
	collision_file_name = ""
	collision_tsx = ""
	collision_firstgid = 0

	object_layer_name = ""
	object_file_name = ""

	override_layer_name = ""
	override_file_name = ""

	has_collision = False
	has_objects = False
	has_override = False

	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-in":
			i += 1
			infilename = sys.argv[i]
		elif sys.argv[i] == "-out":
			i += 1
			outfilename = sys.argv[i]
		elif sys.argv[i] == "-collision":
			i += 1
			collision_layer_name = sys.argv[i]
			has_collision = True
		elif sys.argv[i] == "-terrain":
			i += 1
			terrain_layer_name = sys.argv[i]
		elif sys.argv[i] == "-objects":
			i += 1
			object_layer_name = sys.argv[i]
			has_objects = True
		elif sys.argv[i] == "-override":
			i += 1
			override_layer_name = sys.argv[i]
			has_override = True
		elif sys.argv[i] == "-terrainset":
			i += 1
			terrain_tsx = sys.argv[i]
		elif sys.argv[i] == "-collisionset":
			i += 1
			collision_tsx = sys.argv[i]
		elif sys.argv[i] == "-?" or sys.argv[i] == "-help":
			usage()
			return

	if terrain_layer_name == "" or infilename == "" or outfilename == "" or terrain_tsx == "":
		usage()
		return

	if has_collision == False and has_override == True:
		print("Collision override requires collision layer!!")
		usage()
		return
			
	u = infilename.upper()
	infilename = u

	u = outfilename.upper()
	outfilename = u

	terrain_firstgid = 0
	collision_firstgid = 0

	if has_collision == True and collision_tsx != "":
		tree = ET.parse(collision_tsx)
		root = tree.getroot()
		for child in root:
			if child.get("source") == collision_tsx:
				collision_firstgid = int(child.get("firstgid"))
	
	terrain_file_name = outfilename + ".TER"
	print("Terrain File Name:  " + terrain_file_name)

	if (has_collision):
		collision_file_name = outfilename + ".COL"
		print("Collision File Name:  " + collision_file_name)
	
	if (has_objects):
		object_file_name = outfilename + ".OBJ"
		print("Object File Name:  " + object_file_name)
	
	if (has_override):
		override_file_name = outfilename + ".OVR"
		print("Override File Name:  " + override_file_name)

	print("")
	print("Input File Name: " + infilename)
	print("Output File Name: " + outfilename)

	tree = ET.parse(infilename)

	root = tree.getroot()
	for child in root:
		if child.get("source") == terrain_tsx:
			terrain_firstgid = int(child.get("firstgid"))
	
	if has_collision == True and collision_tsx != "":
		for child in root:
			if child.get("source") == collision_tsx:
				collision_firstgid = int(child.get("firstgid"))

	print("Collision GID: " + str(collision_firstgid))
	print("Terrain GID:  " + str(terrain_firstgid))

	for child in root:
		if child.get("name") == terrain_layer_name:
			export_tile_layer(child, terrain_firstgid, terrain_file_name)
		elif child.get("name") == collision_layer_name and has_collision == True:
			export_collision_layer(child, collision_firstgid, collision_file_name)
		elif child.get("name") == object_layer_name and has_objects == True:
			export_tile_layer(child, terrain_first_gid, object_file_name)
		elif child.get("name") == collision_override_name and has_override == True:
			export_collision_layer(child, collision_firstgid, override_file_name)

def export_tile_layer(layer, gid, fname):
	print("Exporting tile layer:  " + layer.get("name"))
	mapdata = layer.find("data").text.replace("\n", "").split(",")
	
	try:
		o = open(fname, "wb")
	except:
		print("ERROR:  Could not open tile output file" + fname)
		return

	b = bytearray()
	b.append(0)
	b.append(0)

	for i in range(len(mapdata)):
		m = int(mapdata[i])
		if m > 0:
			m = m - gid

		if m > 255:
			print("Over 255:  " + str(m))
			o1 = m & 0x00FF
			o2 = (m & 0xFF00) >> 8
			b.append(o1)
			b.append(o2)
		elif m <= 255:
			b.append(m)
			b.append(0)

	ba = bytes(b)
	o.write(ba)

	o.close()

def export_collision_layer(layer, gid, fname):
	print("Exporting collision layer:  " + layer.get("name"))
	mapdata = layer.find("data").text.replace("\n", "").split(",")

	try:
		o = open(fname, "wb")
	except:
		print("ERROR:  Could not open collision output file" + fname)
		return

	b = bytearray()
	b.append(0)
	b.append(0)

	for i in range(len(mapdata)):
		m = int(mapdata[i])
		if m > 0:
			d = (m - gid)
		else:
			d = m
			
		b.append(d)
		
	ba = bytes(b)
	o.write(ba)

	o.close()

if __name__ == "__main__":
    main()
