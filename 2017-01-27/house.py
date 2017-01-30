from pyplasm import*
import csv
import workshop_10 as w



hwall = 10
scale = .05
hwindow = hwall-(hwall/4.)
dimborder = .4

def readFile(filename):


	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)


def createExternalEnclosure(filename):
	pointsRead = readFile(filename)
	points = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	extWall = STRUCT(points)	
	extWall = S([1,2,3])([scale,scale,scale])(extWall)
	extWall = OFFSET([.2,.2,hwall])(extWall)

	#doors = create_doors("first_house/lines/doors.lines")
	doors = createDoors("lines/doors.lines")
	walls = DIFFERENCE([extWall, doors])

	#windows = create_windows("first_house/lines/windows.lines")
	windows = createWindows("lines/windows.lines")
	walls = DIFFERENCE([walls, windows])

	walls = TEXTURE("texture/texturewall.jpg")(walls)

	return walls

def createInternalPartitions(filename):
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))

	intWall = STRUCT(points)
	intWall = S([1,2,3])([scale,scale,scale])(intWall)
	intWall = OFFSET([.2,.2,hwall])(intWall)

	#doors = create_doors("first_house/lines/doors.lines")
	doors = createDoors("lines/doors.lines")

	walls = DIFFERENCE([intWall, doors])
	walls = TEXTURE("texture/texturewall.jpg")(walls)


	return walls

def createFloor(filename):
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	floor = SOLIDIFY(STRUCT(points))	
	floor = S([1,2,3])([scale,scale,scale])(floor)
	floor = TEXTURE("texture/texturefloor.jpg")(floor)
	

	return floor

def createDoors(filename):

	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))


	points = STRUCT(points)
	doors = S([1,2,3])([scale,scale,scale])(points)
	doors = OFFSET([.01,.4,hwall-(hwall/4.)])(doors)
	doors = STRUCT([T(2)(-.1),doors])
	return doors

def createWindows(filename):
	pointsRead = readFile(filename)
	xaxis = []
	yaxis = []

	temp = 0

	for i in pointsRead:
		if float(i[1])==float(i[3]): #parallelo asse x
			xaxis.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
		if float(i[0])==float(i[2]): #parallelo asse y
			yaxis.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
		
	
	if(len(yaxis)!=0 and len(xaxis)!=0):
		yaxis = STRUCT(yaxis)
		xaxis = STRUCT(xaxis)
		yaxis = PROD([yaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
		yaxis = OFFSET([5,.001,.001])(yaxis)
		xaxis = PROD([xaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
		xaxis = OFFSET([.001,5,.001])(xaxis)

		windows = STRUCT([xaxis,yaxis])
		windows = S([1,2,3])([scale,scale,scale])(windows)
		windows = STRUCT([T(2)(-.01),windows])
	else:
		if(len(xaxis)!=0):
			xaxis = STRUCT(xaxis)
			xaxis = PROD([xaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
			xaxis = OFFSET([.001,5,.001])(xaxis)
			windows = xaxis
			windows = S([1,2,3])([scale,scale,scale])(windows)
			windows = STRUCT([T(2)(-.01),windows])
		if(len(yaxis)!=0):
			yaxis = STRUCT(yaxis)
			yaxis = PROD([yaxis, QUOTE([-((hwall/8.)/scale),hwindow/scale])])
			yaxis = OFFSET([.001,5,.001])(yaxis)
			windows = yaxis
			windows = S([1,2,3])([scale,scale,scale])(windows)
			windows = STRUCT([T(2)(-.01),windows])

	return STRUCT([windows])

def ggplCreateHouse(path_ext_walls,path_int_walls):

	ext = create_external_enclosure(path_ext_walls)
	intP = create_internal_partitions(path_int_walls)
	floor = create_floor(path_ext_walls)
	walls = STRUCT([ext,intP])		
	house = STRUCT([floor, walls])

	return house


