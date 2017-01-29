from pyplasm import*

def getList(verts):
	lines = []
	for i in range(len(verts)-1):
		lines.append([verts[i],verts[i+1]])
	lines.append([verts[len(verts)-1],verts[0]])
	return lines

def createLanding(directions,alfa):
	plane_points = []

	for i in directions:
		new_point = []
		if(i[1]==1): 
			new_point.append(i[0][0]+30*math.cos(PI/4))
			new_point.append(i[0][1]+30*math.sin(PI/4))
			
		if(i[1]==2): 
			new_point.append(i[0][0]-30*math.cos(PI/4))
			new_point.append(i[0][1]+30*math.sin(PI/4))
			
		if(i[1]==3): 
			new_point.append(i[0][0]-30*math.cos(PI/4))
			new_point.append(i[0][1]-30*math.sin(PI/4))
			
		if(i[1]==4): 
			new_point.append(i[0][0]+30*math.cos(PI/4))
			new_point.append(i[0][1]-30*math.sin(PI/4))
			
		new_point.append(i[0][2]+30*math.sin(alfa))
		plane_points.append(new_point)

	points = []
	for i in plane_points:
		points.append(i)
	points.append(plane_points[0])
	return points

def createValley(verts,directions):
	points = createLanding(directions,alfa)

	segmUp = getList(points)
	segmDown = getList(verts)

	if (len(segmDown) == len(segmUp)):
		listFalde = []
		for i in range(len(segmUp)-1):
			
			verts_temp = []
			hpc = 0
			verts_temp.append(segmUp[i][0])
			verts_temp.append(segmUp[i][1])
			verts_temp.append(segmDown[i][0])
			verts_temp.append(segmDown[i][1])
			hpc = MKPOL([verts_temp,[[1,2,3,4]],1])
			listFalde.append(hpc)

	return STRUCT(listFalde)

def createRoof(verts, cells, alfa, directions):

	points_landing = createLanding(directions,alfa) 
	landing = MKPOL([points_landing,cells,1])
	flaps = createValley(verts, directions)
	
	roof = STRUCT([landing, flaps])
	roof = OFFSET([.4,.4])(roof)
	roof = TEXTURE("texture/roof.jpg")(roof)
	print(UKPOL(roof))
	return roof

verts = [[0,0,0],[6,0,0],[6,6,0],[3,6,0],[3,3,0],[0,3,0],[0,0,0]]
cells = [[1,2,5,6],[2,3,4,5]]

directions = [[[0,0,0],1],[[6,0,0],2],[[6,6,0],3],[[3,6,0],4],[[3,3,0],4],[[0,3,0],4]]

alfa = PI/3
