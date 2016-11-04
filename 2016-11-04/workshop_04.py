from pyplasm import *

def ggpl_roofBuilder(roofShape):
	
	sk1 = SKEL_1(roofShape)
	sk2 = SKEL_2(roofShape)

	ukpol = UKPOL(sk2)
	offset = OFFSET([.1,.1,.1])(sk1)

	vertices = ukpol[0]

	for j in ukpol[1]:
		vertices = []
		
		for i in j:
			vertices.extend([ukpol[0][i-1]])
			
		
		if len(j) == 3:
			offset = STRUCT([offset,OFFSET([.1,.1,.1])(MKPOL([vertices,[[1,2,3]],None]))])

		else:
			z = vertices[0][2]
			for k in vertices:
				if z != k[2]:
					offset = STRUCT([offset,OFFSET([.1,.1,.1])(MKPOL([vertices,[[1,2,3,4]],None]))])

	return offset

def hipRoof():
	vertices = [[0,0,0],[4,0,0],[2,1,2],[2,5,2],[0,6,0],[4,6,0]]
	cells = range(1,7)
	input = MKPOL([vertices,[cells],None])
	return input

def hippedLShaped():
	vertices1 = [[10,0,0],[9,2,2],[10,4,0],[0,0,0],[2,2,2],[4,4,0]]
	vertices2 = [[0,0,0],[2,2,2],[4,4,0],[0,7,0],[2,6,2],[4,7,0]]
	cells = range(1,10)
	input1 = MKPOL([vertices1,[cells],None])
	input2 = MKPOL([vertices2,[cells],None])
	return STRUCT([input1,input2])

VIEW(ggpl_roofBuilder(hippedLShaped()))