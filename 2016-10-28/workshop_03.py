from pyplasm import *
"""This function returns a hpc value containing a U-shaped stair"""
def ggpl_uShapedStair(dx,dy,dz):

	numberOfSteps = int(dz/.18)
	riser = float(dz)/numberOfSteps
	tread = .64-2*riser

	step = CUBOID([float(dx)/2,tread,riser])

	"""Create the first ramp"""
	for i in range(1,numberOfSteps/2):
		step = STRUCT([step, T(2)(tread), T(3)(riser), step])

	landing = CUBOID([dx,float(dy)/4,riser])
	stair = STRUCT([step,T(2)(tread*numberOfSteps/2),T(3)(riser*numberOfSteps/2),landing])
	step = CUBOID([float(dx)/2,tread,riser])

	a = CUBOID([float(dx)/2,tread,float(dz)/4])


	understair = MKPOL([[[0,0],[tread,riser],[0,riser]],[[1,2,3]],1])
	width = QUOTE([float(dx)/2])
	understairs = PROD([understair,width])
	understairs = STRUCT([R([1,3])(-PI/2)(understairs)])
	understairs = STRUCT([R([2,3])(PI/2)(understairs)])
	understairs = STRUCT([T(2)(tread),understairs])

	for i in range(1,numberOfSteps/2-1):
		understairs = STRUCT([understairs, T(2)(tread), T(3)(riser),understairs])


	understair = STRUCT([R([1,2])(PI),understairs])
	understair = STRUCT([T([1,2,3])([dx,tread*.5+dy*.75,float(dz)/2]), understair])
	"""Create the second ramp"""
	for i in range(1, numberOfSteps/2):
		stair = STRUCT([stair,T(1)(float(dx)/2),T(2)(tread*numberOfSteps/2-tread*i),T(3)(riser*numberOfSteps/2+riser*i),step])
	stair = STRUCT([understairs,stair])

	stair = STRUCT([understair,stair])
	VIEW(stair)
	

ggpl_uShapedStair(4,3,3)