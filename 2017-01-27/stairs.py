from pyplasm import*
import math


def straightStairs(width, tread, riser, nStep):

	xStep = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
	step =  PROD([QUOTE([width]), xStep])

	
	firstStep = CUBOID([width,tread,riser])

	stairsList=[]
	stairsList.append(firstStep)

	tempy = 0
	tempz = 0
	for i in range(nStep-1):
		trasl = STRUCT([T(2)(tempy),T(3)(tempz), step]) #every step there is a traslation
		stairsList.append(trasl)
		tempy = tread+tempy
		tempz = riser+tempz

	return STRUCT(stairsList)

def ggplStraightStairs(dx, dy, dz):

	yStep = .5
	xStep = dx 	
	
	nStep = int(dy/yStep)
	zStep = (float(dz)/float(nStep))

	wall = CUBOID([0.1,dy,dz]) #create walls close to stairs
	
	stairs = straightStairs(xStep,yStep,zStep,nStep)
	
	return stairs
