from pyplasm import *

"""Create a door from x,y and z parameters"""
def door(dx,dy,dz):

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([dx-(dx/4.),dy/4.,dz-(dz/4.)])
	c1 = STRUCT([T([1,3])([(dx/4.)/2.,(dz/4.)/2.]),c1])
	c2 = STRUCT([T([2])([dy-(dy/4.)]),c1])
	door = DIFFERENCE([c,STRUCT([c1,c2])])
	door = TEXTURE("texture/floor.jpg")(door)
	return door