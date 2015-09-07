import numpy as np
from numpy.polynomial import polynomial as P
import matplotlib.pyplot as plt
import re
import scipy as S

convertPressure = -160.05

volume_sc = []
energy_sc = []

volume_bcc = []
energy_bcc = []

volume_fcc = []
energy_fcc = []

volume_sn = []
energy_sn = []

#read fcc data
fccVolFile = open("fcc/min/volume.txt", "r")
#fccVolFile = open("fcc/gga/volume.txt", "r")

for line in fccVolFile:
	volume_fcc.append(float(line)/4)

fccEnFile = open("fcc/min/energy.txt", "r")
#fccEnFile = open("fcc/gga/energy.txt", "r")

for line in fccEnFile:
	energy_fcc.append(float(line)/4)

#read bcc data
bccVolFile = open("bcc/min/volume.txt", "r")
#bccVolFile = open("bcc/gga/volume.txt", "r")

for line in bccVolFile:
	volume_bcc.append(float(line)/2)

bccEnFile = open("bcc/min/energy.txt", "r")
#bccEnFile = open("bcc/gga/energy.txt", "r")

for line in bccEnFile:
	energy_bcc.append(float(line)/2)

#read sc data

scVolFile = open("sc/min/volume.txt", "r")
#scVolFile = open("sc/gga/volume.txt", "r")

for line in scVolFile:
	volume_sc.append(float(line))

scEnFile = open("sc/min/energy.txt", "r")
#scEnFile = open("sc/gga/energy.txt", "r")

for line in scEnFile:
	energy_sc.append(float(line))

#read Sn data

snVolFile = open("beta/min/volume.txt", "r")
#scVolFile = open("sc/gga/volume.txt", "r")

for line in snVolFile:
	volume_sn.append(float(line)/4)

snEnFile = open("beta/min/energy.txt", "r")
#scEnFile = open("sc/gga/energy.txt", "r")

for line in snEnFile:
	energy_sn.append(float(line)/4)

#fitted polynomial
poly_fcc = np.poly1d(np.polyfit(volume_fcc, energy_fcc,5))
poly_bcc = np.poly1d(np.polyfit(volume_bcc, energy_bcc,9))
poly_sc =  np.poly1d(np.polyfit(volume_sc,  energy_sc, 8))
poly_sn =  np.poly1d(np.polyfit(volume_sn,  energy_sn, 9))

#energy corresponding to volume vol
vol = np.linspace(10,60,50)

en_fcc = poly_fcc(vol)
en_bcc = poly_bcc(vol)
en_sc  = poly_sc(vol)
en_sn = poly_sn(vol)

def plot_raw_data():
	#Graph output
	plt.plot(volume_fcc, energy_fcc, 'bo', label='FCC')
	plt.plot(vol, en_fcc, 'b', label='FCC_FIT')

	plt.plot(volume_sc, energy_sc, 'r^', label='SC')
	plt.plot(vol, en_sc, 'r-', label='SC_FIT')

	plt.plot(volume_bcc, energy_bcc, 'gs', label='BCC')
	plt.plot(vol, en_bcc, 'g--', label='BCC_FIT')

	plt.plot(volume_sn, energy_sn, 'yo', label='beta-Sn')
	plt.plot(vol, en_sn, 'y-.', label='beta-Sn_FIT')

	plt.ylabel('U [eV]')
	plt.xlabel('V [A**3]')

	plt.ylim(-1005,-1000.2)
	plt.xlim(20,60)
	plt.legend()

pres_fcc = np.polyder(poly_fcc)
pres_bcc = np.polyder(poly_bcc)
pres_sc  = np.polyder(poly_sc)
pres_sn  = np.polyder(poly_sn)


#print pres_fcc

enth_fcc = en_fcc + vol*pres_fcc(vol)
enth_bcc = en_bcc + vol*pres_bcc(vol)
enth_sc  = en_sc  + vol*pres_sc(vol)
enth_sn  = en_sn  + vol*pres_sn(vol)

#print enth_fcc
#print pres_fcc(vol)

def plot_ethalpy_pressure():
	plt.plot(convertPressure*pres_fcc(vol),enth_fcc, 'b-', label='FCC')
	plt.plot(convertPressure*pres_sc(vol), enth_sc,  'r-', label='SC')
	plt.plot(convertPressure*pres_bcc(vol),enth_bcc, 'g-', label='BCC')
	plt.plot(convertPressure*pres_sn(vol), enth_sn,  'y-', label='beta-Sn')
	plt.ylabel('H [eV]')
	plt.xlabel('P [GPa]')
	plt.legend()

#Bulk Modulus
b_poly_fcc = np.polyder(poly_fcc, 2)
b_poly_sc = np.polyder(poly_sc, 2)
b_poly_bcc = np.polyder(poly_bcc, 2)
b_poly_sn = np.polyder(poly_sn, 2)

bulk_fcc = vol*b_poly_fcc(vol)
bulk_sc  = vol*b_poly_sc(vol)
bulk_bcc = vol*b_poly_bcc(vol)
bulk_sn  = vol*b_poly_sn(vol)

#print bulk_bcc - bulk_fcc

#def plot_bulk_mod():
#	plt.plot(vol,bulk_fcc, 'b-', label='FCC')
#	plt.plot(vol,bulk_sc,  'r-', label='SC')
#	plt.plot(vol,bulk_bcc, 'g-', label='BCC')
#	plt.plot(vol,bulk_sn,  'y-', label='beta-Sn')
#	plt.legend()

plot_raw_data()
#plot_bulk_mod()
plt.show()


plot_ethalpy_pressure()
plt.show()

