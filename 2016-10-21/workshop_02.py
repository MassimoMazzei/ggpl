import csv


"""This function returns a 3d value of type HPC representing the bone structure of a reinforce concrete building"""
def ggpl_bone_structure(file_name):
	reader = csv.reader(file(file_name, "rb"))
	for row in reader:
		print row[0]
ggpl_bone_structure("frame_data_451631.csv")