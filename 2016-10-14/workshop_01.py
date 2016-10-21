from pyplasm import *

def spaceFrame(bx, bz, px, py, pillarDistances, pillarHeights):

	def createPillars(distance, height):
		pillar = CUBOID([px, py, height])
		pillar = STRUCT([T(3)(distance), pillar])
		pillars = STRUCT([pillar, T(2)(pillarDistances[0]), pillar])
		dist = pillarDistances[0]
		for i in pillarDistances[1:]:
			pillars = STRUCT([pillars, T(2)(dist + i), pillar])
			dist = dist + i
		return pillars

	def createBeams(height):
		beam = CUBOID([bx, pillarDistances[0], bz])
		beams = STRUCT([T(3)(height), T(2)(px/2), beam])
		dist = pillarDistances[0]
		for i in pillarDistances[1:]:
			beam = CUBOID([bx, i, bz])
			beams = STRUCT([beams, T(3)(height), T(2)(dist + px/2), beam])
			dist = dist + i
		return beams

	def addFloor (structure, distance, pillarHeight):
		return STRUCT([structure, createPillars(distance, pillarHeight), createBeams(distance + pillarHeight)])

	def createGroundFloor():
		return STRUCT([createPillars(0,pillarHeights[0]), createBeams(pillarHeights[0])])

	def createStructure():
		structure = createGroundFloor()
		distance = pillarHeights[0]
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