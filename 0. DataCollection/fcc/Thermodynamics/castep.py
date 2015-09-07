import re
import subprocess

volumeList = []
energyList = []

lattice_Param = 3.715134
lattice_zero = 0
lattice_deg = 90.0

def writeDotCell():
	#Write the Ca.cell file
	outputfile = open("Ca.cell", "w")

	outputfile.write("%BLOCK LATTICE_ABC\n")
	outputfile.write("            " + str(lattice_Param) + "       " + str(lattice_Param) + "       " + str(lattice_Param) + "\n")
	outputfile.write("            " + str(lattice_deg) + "            " + str(lattice_deg) + "            " + str(lattice_deg) + "\n")
	outputfile.write("%ENDBLOCK LATTICE_ABC\n\n")  

	outputfile.write("%BLOCK POSITIONS_FRAC\n")
	outputfile.write("Ca                  0       0         0\n")
	outputfile.write("Ca		      0       0.5     0.5\n")
	outputfile.write("Ca		      0.5     0       0.5 \n")
	outputfile.write("Ca		      0.5     0.5       0\n")
	outputfile.write("%ENDBLOCK POSITIONS_FRAC\n\n")

	outputfile.write("KPOINTS_MP_GRID 	  	4	4	4\n\n")
	outputfile.write("phonon_kpoint_mp_grid		2	2	2 \n\n")
	outputfile.write("supercell_kpoint_mp_grid  	2	2	2\n\n")

	outputfile.write("%block phonon_fine_kpoint_path\n")
	outputfile.write("0.0 0.0 0.0 		! Gamma\n")
	outputfile.write("0.0	0.5	0.5 		!X\n")
	outputfile.write("0.25	0.75	0.5		!W\n")
	outputfile.write("0.375	0.75	0.375		!K\n")
	outputfile.write("0.0	0.0	0.0 		!Gamma\n")
	outputfile.write("0.5	0.5	0.5 		!L\n")
	outputfile.write("0.25	0.625	0.625		!U\n")
	outputfile.write("0.25	0.75	0.5		!W\n")
	outputfile.write("0.5	0.5	0.5 		!L\n")
	outputfile.write("0.0	0.0	0.0 		!Gamma\n")
	outputfile.write("0.25	0.625	0.625		!U\n")
	outputfile.write("0.0	0.5	0.5 		!X\n")
	outputfile.write("%endblock phonon_fine_kpoint_path\n\n")

	outputfile.write("symmetry_generate\n\n")

	outputfile.write("%block PHONON_SUPERCELL_MATRIX \n")
	outputfile.write("2 0 0\n")
	outputfile.write("0 2 0\n")
	outputfile.write("0 0 2\n")
	outputfile.write("%endblock PHONON_SUPERCELL_MATRIX \n")

	outputfile.close()


def runCastep():
	subprocess.call("castep Ca", shell=True)

for x in range(0,5): 
	writeDotCell()
	print str(x) + ": Running Castep..."
	runCastep()
	print "Castep done"

	lattice_Param -= 0.3
	writeDotCell()
	print "Ready: \n\n"

castepFile = open("Ca.castep", "r")

for line in castepFile:

	if re.search( r"volume =", line):
		words = line.split()
		volumeList.append(float(words[4]))

	if re.search( r"NB est. ", line):
		ener = line.split()
		print ener[6]
		energyList.append(float(ener[6]))

#print volumeList
#print energyList

volumeFile = open("volume.txt", "w")
for item in volumeList:
	volumeFile.write(str(item) + "\n")
volumeFile.close()

energyFile = open("energy.txt", "w")
for item in energyList:
	energyFile.write(str(item) + "\n")
energyFile.close()




