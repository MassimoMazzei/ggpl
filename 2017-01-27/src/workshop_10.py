from pyplasm import *
from larlib import *
import roof as r
import house as h
import window as w
import door as d
import csv
import stairs as s


	



"""Read a file from the filename """
def readFile(filename):
	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)


"""Create the doors from the doors.line file"""
def createDoors(filename):

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	doors = []

	for i in reader:
		if(i[1]==i[3]):
			door = d.door(i[2]-i[0],4,hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)
		else:
			door = d.door(4,i[3]-i[1],hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)

	doors = STRUCT(doors)
	doors = S([1,2,3])([scale,scale,scale])(doors)

	return doors


"""Create the windows from the windows.lines file"""
def createWindows(filename):

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]
	windows = []
	for i in reader:
		if(i[1]==i[3]):
			if(i[2]>i[0]):
				window = w.window(i[2]-i[0],5,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			else:
				window = w.window(i[0]-i[2],5,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[2],i[1],((hwall/8.)/scale)]),window]) 		
			
		if(i[0]==i[2]):
			if(i[3]>i[1]):
				window = w.window(i[3]-i[1],5,hwindow/scale)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
				
			else:
				window = w.window(i[1]-i[3],5,hwindow/scale)
				window = R([1,2])(PI/2.)(window)
				window = STRUCT([T([1,2,3])([i[0]+5,i[1],((hwall/8.)/scale)]),window])
					
		windows.append(window)

	windows = STRUCT(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)
	return windows


"""Create the roof from the roof.lines file"""
def createRoof(filename):
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	points = []
	for i in reader:
		points.append([i[0],i[1],0])
	points.append([reader[0][0],reader[0][1]])

	cells = [[1,2,3,4]]
	directions = []
	directions.append([points[0],1])
	directions.append([points[1],2])
	directions.append([points[2],3])
	directions.append([points[3],4])

	print points
	roof = r.createRoof(points,cells,roofAngle,directions)
	roof = S([1,2,3])([scale+.001,scale+.001,scale])(roof)

	return roof


"""Create the stairs from the stair.lines file"""	
def createStairs(filename):
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]
	dx=0
	dy=0
	tx = reader[0][0]*scale
	ty = reader[0][1]*scale
	for i in reader:
		if i[1]==i[3]: 
			dx = (i[2]-i[0])*scale
		if i[0]==i[2]: 
			dy = (i[3]-i[1])*scale
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy

	stairs = s.ggplStraightStairs(dx,dy,hwall)
	stairs = R([1,2])(PI)(stairs)
	stairs = STRUCT([T([1,2])([tx+dx,ty+dy]),stairs])

	stairs = TEXTURE("texture/stairs.jpg")(stairs)

	return stairs




def createUpperFloor(walls,parquet,path_stairs):

	reader = readFile(path_stairs)
	reader = [[float(float(j)) for j in i] for i in reader]

	hole = []
	for i in reader:
		hole.append(POLYLINE([[i[0],i[1]],[i[2],i[3]]]))
	hole = SOLIDIFY(STRUCT(hole))

	hole = S([1,2,3])([scale,scale,scale])(hole)
	hole = OFFSET([.01,.01,.1])(hole)
	floor = DIFFERENCE([parquet,hole])
	
	floor = TEXTURE("texture/floor.jpg")(floor)
	intfloor = STRUCT([floor, walls])

	return intfloor

"""Create a floor of the house"""
def createFloor(path_ext_walls,path_int_walls,path_stairs,path_windows,path_doors,flag):

	ext_walls = h.createExternalEnclosure(path_ext_walls)

	int_walls = h.createInternalPartitions(path_int_walls)
	walls = STRUCT([ext_walls, int_walls])
	parquet = OFFSET([.1,.1,.1])(h.createFloor(path_ext_walls))
	doors = createDoors(path_doors)
	windows = createWindows(path_windows)
	if flag=='i':

		#win = windows
		ext = SKEL_1(BOX([1,2])(ext_walls))
		ext = PROD([ext,QUOTE([hwall])])
		ext = OFFSET([.01,.01,.01])(ext)
		windows = OFFSET([.1,.1,.1])(windows)
		ext = DIFFERENCE([ext,windows])
		winx = STRUCT([T(1)(-.2),windows])
		ext = DIFFERENCE([ext,winx])
		winy = STRUCT([T(2)(-.2),windows])
		ext = DIFFERENCE([ext,winy])
		windows = createWindows(path_windows)
		walls = STRUCT([ext, int_walls])
		walls = TEXTURE("texture/wall.jpg")(walls)

		floor = createUpperFloor(walls,parquet,path_stairs) 
		floor = STRUCT([floor, windows])
		return STRUCT([T(3)(hwall),floor])
	if flag=='g':
		parquet = TEXTURE("texture/floor.jpg")(parquet)
		walls = TEXTURE("texture/wall.jpg")(walls)
		return STRUCT([walls,parquet, windows, doors])

scale = .05					
hwall= 10					
hdoor = hwall-(hwall/4.)	
hwindow = hwall-(hwall/4.)	
roofAngle = 60*PI/180	

def main():
	
	ground = createFloor("lines/external.lines","lines/internal.lines","lines/stairs.lines","lines/windows.lines","lines/doors.lines",'g')
	floor1 = createFloor("lines/external.lines","lines/internal.lines","lines/stairs.lines","lines/windows.lines","lines/doors.lines",'i')
	stairs = createStairs("lines/stairs.lines")

	roof = STRUCT([T(3)(hwall*2),createRoof("lines/external.lines")])

	VIEW(STRUCT([ground, stairs, floor1, roof]))
	
if __name__ == '__main__':
    main()

