import csv
from pyplasm import *

"""This function returns a 3d value of type HPC representing the bone structure of a reinforce concrete building"""
def ggpl_bone_structure(file_name):


        
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


	def readFile():
		reader = csv.reader(file(file_name, "rb"))
		i = 1
		vectorX = 0
		vectorY = 0
		vectorZ = 0
		frames = []
		for row in reader:
			if i % 2 == 1:
				vectorX = float(row[0]) + vectorX
				vectorY = float(row[1]) + vectorY
				vectorZ = float(row[2]) + vectorZ
				vector = [vectorX, vectorY, vectorZ]
			else:
				a = 0
				parameters = []
				for elem in row:
					values = elem.split(",")
					parameters.append(values)


				bx = float(parameters[0][0])
				bz = float(parameters[1][0])
				px = float(parameters[2][0])
				py = float(parameters[3][0])
				distances = []
				heights = []
				for p in parameters[4]:
					distances.append(float(p))
				for p in parameters[5]:
					heights.append(float(p))

				frame = spaceFrame(bx, bz, px, py, distances, heights)
				frame = STRUCT([T(0)(vectorX), T(1)(vectorY), T(2)(vectorZ), frame])
				

				frames.append(frame)
			i = i + 1
		return frames
		
	def createStructure():
		parameters = readFile()
		structure = parameters[0]
		for frame in parameters[1:]:
			structure = STRUCT([structure, frame])

		beamX = [0.2, -1.3, 0.2, -1.3, 0.2]
		beamZ = [10.2]
		beamY = [-1, 0.2, -.8, 0.2, -.8, 0.2, -.8, 0.2, -.8, 0.2, -.8, 0.2]
		beam1DX = QUOTE(beamX)
		beam1DY = QUOTE(beamY)
		beam1DZ = QUOTE(beamZ)
		beam2D = PROD([beam1DX, beam1DY])
		beam3D = PROD([beam1DZ, beam2D])
		structure = STRUCT([beam3D, structure])
		return structure

	VIEW(createStructure())
	
ggpl_bone_structure("frame_data_451631.csv")
