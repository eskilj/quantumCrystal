# quantumCrystal

Quantum Calculation of High Pressure Crystal Structures

Overview:

0.	DataCollection 		- Contain the CASTEP files and python scrips for the different crystal structures. </br>
		GeometryOpt 	- Single point energy calculations </br>
		Thermodynamics 	- Phonon and thermodynamic calculations </br>

1. DataHandling    		- Contains the code used in processing the data </br>
		GeoOpt.py 	    - Script used for gathering and plotting the geometry optimisation data. First Energy vs Volume, and then Enthalpy vs Pressure. </br>
		FreeEnergy.py 	- Script used for processing the geometric and thermodynamic data, to lastly produce the gibbs.txt, which indicates stable structure at given pressure and temperature. </br>
		disperison.pl 	- plots phonon dispersion </br>
		dos.pl 		    - plots phonon density of states </br>
		qha.py 		    - Python script used to calculate structural properties: Bulk modulus etc. (need a ev.dat file with energy and volume data) </br>
		
		
