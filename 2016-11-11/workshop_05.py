from pyplasm import *
from fpformat import fix
def ggpl_furniture():
	def color(r,g,b):
	    return [float(fix(r/255.,6)),float(fix(g/255.,6)),float(fix(b/255.,6)),1.000000]
	
	deskX = 1.0
	deskY = 0.5
	deskZ = 0.1
	legX = .05
	legY = .05
	desk = CUBOID([deskX, deskY, deskZ])
	leg = CUBOID([legX, legY, deskZ])

	desk = STRUCT([leg,T(3)(deskZ), desk])
	desk = STRUCT([desk,T(1)(deskX-legX), leg])
	desk = STRUCT([desk,T(2)(deskY-legY), leg])
	desk = STRUCT([desk,T([1,2])([deskX-legX, deskY-legY]), leg])
	



	chairX = .5
	chairY = .5
	chairZ = .05
	chairLegX = .05
	chairLegY = .05
	chairLegZ = .5
	chairBackX = .5
	chairBackY = .05
	chairBackZ = .6

	chairBack = CUBOID([chairBackX, chairBackY, chairBackZ])
	chairLeg = CUBOID([chairLegX, chairLegY, chairLegZ])
	chair = CUBOID([chairX, chairY, chairZ])
	
	VIEW(chair)
	chair = STRUCT([chairLeg, T(3)(chairLegZ), chair])
	chair = STRUCT([chair,T(1)(chairX-chairLegX), chairLeg])
	chair = STRUCT([chair, T(2)(chairY-chairLegY), chairLeg])
	chair = STRUCT([chair, T([1,2])([chairX-chairLegX,chairY-chairLegY]), chairLeg])
	chair = STRUCT([chair, T(3)(chairLegZ+chairZ), chairBack])

	VIEW(chair)
	blackboardX = 2.0
	blackboardY = .08
	blackboardZ = 1.4
	baseX = .05
	baseY = .4
	baseZ = .05
	legX = .05
	legY = .05
	legZ = 2

	base = CUBOID([baseX,baseY,baseZ])
	leg = CUBOID([legX,legY,legZ])
	pedestal = STRUCT([base,T([2,3])([baseY/2-legY/2,baseZ]),leg])
	pedestal = STRUCT([pedestal,T(1)(blackboardX),pedestal])

	blackboard = CUBOID([blackboardX,blackboardY,blackboardZ])
	blackboard = COLOR(color(112,128,144))(blackboard)

	blackboard = STRUCT([pedestal,T([2,3])([baseY/2-blackboardY/2,legZ/2]),blackboard])
	


	structure = STRUCT([chair,T([1,2])([-chairX/2,chairY+.1]),desk])
	

ggpl_furniture()