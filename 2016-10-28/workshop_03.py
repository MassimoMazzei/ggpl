from pyplasm import *
"""This function returns a hpc value containing a U-shaped stair"""
def ggpl_uShapedStair(dx,dy,dz):

	numberOfSteps = int(dz/.18)
	riser = float(dz)/numberOfSteps
	tread = .64-2*riser

	def createStep():
		step = CUBOID([float(dx)/2,tread,riser])
		return step

	step = createStep()

	"""Create the first ramp"""
	for i in range(1,numberOfSteps/2):
		step = STRUCT([step, T(2)(tread), T(3)(riser), step])

	landing = CUBOID([dx,float(dy)/4,riser])
	stair = STRUCT([step,T(2)(tread*numberOfSteps/2),T(3)(riser*numberOfSteps/2),landing])
	step = createStep()

	a = CUBOID([float(dx)/2,tread,float(dz)/4])

	#H = MAT([[1,0,0],[0,1,0],[0,float(dy)/2,1]])
	#m = STRUCT([SKEL_1(a), H, a])
	#m = STRUCT([R([1,3])(PI/2)(m)])
	#m = STRUCT([T(1)(float(dx)/2),m])
	#m = STRUCT([T(2)(tread/2),m])

	"""Create the second ramp"""
	for i in range(1, numberOfSteps/2):
		stair = STRUCT([stair,T(1)(float(dx)/2),T(2)(tread*numberOfSteps/2-tread*i),T(3)(riser*numberOfSteps/2+riser*i),step])
	#f = STRUCT([m,stair])
	VIEW(stair)
	

ggpl_uShapedStair(3,3,3)