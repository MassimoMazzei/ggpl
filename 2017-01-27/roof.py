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
	return roof

verts = [[0,0,0],[6,0,0],[6,6,0],[3,6,0],[3,3,0],[0,3,0],[0,0,0]]
cells = [[1,2,5,6],[2,3,4,5]]

directions = [[[0,0,0],1],[[6,0,0],2],[[6,6,0],3],[[3,6,0],4],[[3,3,0],4],[[0,3,0],4]]

alfa = PI/3

def roofBuilder(points,alpha):
    h = 15.0
    #Calcolo della distanza tra i punti esterni e i punti interni
    space = math.atan2(h,1/math.sin(alpha))

    xMin = xMax = yMin = yMax = 0
    for i in points:
        if i[0] > xMax:
            xMax = i[0]
        elif i[0] < xMin:
            xMin = i[0]
        elif i[1] > yMax:
            yMax = i[1]
        elif i[1] < yMin:
            yMin = i[1]
    
    #Calcolo dei punti alti del tetto
    higherPoints = []
    for i in range(0,len(points)):
        x = y = 0
        if points[i][0] == xMax:
            x = points[i][0]-space
        elif points[i][0] == xMin or (points[i-1][0] <= points[i][0] and  points[i+1][0] >= points[i][0]):
            x = points[i][0]+space
        
        if points[i][1] == yMin:
            y = points[i][1]+space
        elif points[i][1] == yMax or (points[i-1][1] <= points[i][1] and points[i+1][1] >= points[i][0]):
            y = points[i][1]-space
        point = [x,y]
        higherPoints.extend([point])
    
    #Crezione del soffitto del tetto
    ceiling = STRUCT(AA(POLYLINE)([[higherPoints[0],higherPoints[1],higherPoints[2],higherPoints[3],higherPoints[0]]]))
    ceiling = SOLIDIFY(ceiling)
    ceiling = STRUCT([T(3)(h),ceiling])
    
    for p in points:
        p.append(0)
    for hp in higherPoints:
        hp.append(h)
    newPoints = points+higherPoints
    
    #Creazione delle celle del tetto
    newCells = []
    for j in range(1,len(points)+1):
        if j != len(points):
            newCells.extend([[j,j+1,j+len(points),j+len(points)+1]])
        else:
            newCells.extend([[j,1,j+len(points),j+1]])
    
    #Creazione del modello
    roof = MKPOL([newPoints,newCells,None])
    roof = STRUCT([roof,ceiling])
    roof = OFFSET([.1,.1,.1])(roof)
    roof = COLOR(RED)(roof)
    
    
    VIEW(roof)
    return roof