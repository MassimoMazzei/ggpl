from pyplasm import *

def spaceFrame(bx, bz, px, py, pillarDistances, pillarHeights):

	def createPillars(distance, height):
		a = CUBOID([px, py, height])
		a = STRUCT([T(3)(distance), a])
		b = STRUCT([a, T(2)(pillarDistances[0]), a])
		dist = pillarDistances[0]
		for i in pillarDistances[1:]:
			b = STRUCT([b, T(2)(dist + i), a])
			dist = dist + i
		return b

	def createBeams(height):
		a = CUBOID([bx, pillarDistances[0], bz])
		
		b = STRUCT([T(3)(height), T(2)(px/2), a])
		dist = pillarDistances[0]
		for i in pillarDistances[1:]:
			a = CUBOID([bx, i, bz])
			b = STRUCT([b, T(3)(height), T(2)(dist + px/2), a])
			dist = dist + i
		return b

	def addFloor (structure, distance, pillarHeight):
		return STRUCT([structure, createPillars(distance, pillarHeight), createBeams(distance + pillarHeight)])

	def createGroundFloor():
		return STRUCT([createPillars(0,pillarHeights[0]), createBeams(pillarHeights[0])])

	def createStructure():
		structure = createGroundFloor()
		distance = pillarHeights[0] + bz
		for i in pillarHeights:
			structure = addFloor(structure, distance, i)
			distance = distance + i
			
		return structure

	return createStructure()


	


bx = .4
bz = .4
px = .4
py = .4
pillarDistances = [4, 5, 4, 4.5, 5]
pillarHeights = [3, 2, 3, 5]


VIEW(spaceFrame(bx, bz, px, py, pillarDistances, pillarHeights))