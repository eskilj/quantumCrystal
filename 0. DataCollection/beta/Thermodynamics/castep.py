#Sn fcc

import re
import scipy as S
import subprocess

volumeList = []
energyList = []

lattice_Param_ab = 5.365356
rel = 3.574644 / 6.865356
lattice_Param_c = lattice_Param_ab * rel
lattice_deg = 90
lattice_zero = 0


def writeDotCell():
	#Write the Ca.cell file
	outputfile = open("Ca.cell", "w")

	outputfile.write("%BLOCK LATTICE_ABC\n")
	outputfile.write("            " + str(lattice_Param_ab) + "       " + str(lattice_Param_ab) + "       " + str(lattice_Param_c) + "\n")
	outputfile.write("            " + str(lattice_deg) + "            " + str(lattice_deg) + "            " + str(lattice_deg) + "\n")
	outputfile.write("%ENDBLOCK LATTICE_ABC\n\n")

	outputfile.write("%BLOCK POSITIONS_FRAC\n")
	outputfile.write("Ca                  0.0              0.0                   0.0\n")
	outputfile.write("Ca                  0.5              0.5                   0.5\n")
	outputfile.write("Ca                  0.5              0.0                   0.75\n")
	outputfile.write("Ca                  0.0              0.5                   0.25\n")
	outputfile.write("%ENDBLOCK POSITIONS_FRAC\n\n")

	outputfile.write("KPOINTS_MP_GRID 2 2 2\n\n")
	outputfile.write("supercell_kpoint_MP_GRID 2 2 2\n\n")
	outputfile.write("phonon_kpoint_mp_grid		2	2	2\n\n")

	outputfile.write("%block phonon_fine_kpoint_path\n")
	outputfile.write("0.0 0.0 0.0\n")
	outputfile.write("-0.5 0.5 0.5\n")
	outputfile.write("0.25 0.25 0.25\n")
	outputfile.write("0.0 0.0 0.0\n")
	outputfile.write("0.0 0.5 0.0\n")
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

#	lattice_pressure += 2
	lattice_Param_ab -= 0.3
 	lattice_Param_c = rel * lattice_Param_ab
	writeDotCell()
	print "Ready: \n\n"

