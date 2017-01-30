from pyplasm import *

"""Create a window from x,y and z parameters"""
def window(dx,dy,dz):

	dimborder = 1

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([(dx-(3*dimborder))/2.,dy,(dz-(3*dimborder))/2.])
	c2 = STRUCT([T([1,3])([dimborder,dimborder]),c1,T([1])([((dx-(3*dimborder))/2.)+dimborder]),c1])
	c3 = STRUCT([c2, T(3)([((dz-(3*dimborder))/2.)+dimborder]),c2])

	borders = STRUCT([DIFFERENCE([c,c3])])
	glasses = STRUCT([T(2)(3*(dy/8.)),CUBOID([dx,dy/4.,dz])])
	borders = TEXTURE("texture/floor.jpg")(borders)
	glasses = TEXTURE("texture/glass.jpg")(glasses)

	window = STRUCT([borders,glasses])
	return window