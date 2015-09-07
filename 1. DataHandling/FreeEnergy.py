import numpy as np
import pylab as pl
from numpy.polynomial import polynomial as P
import matplotlib.pyplot as plt
import re
import scipy as S
import math
from scipy import interpolate

from mpl_toolkits.mplot3d import Axes3D

#Generic Variables
convertPressure = -160.05
temp = []

tempFile = open("sc/data/temp.txt", "r")
for line in tempFile:
	temp.append(float(line))
tempFile.close()

#Import data: SC

pt_plot = []
press_sc = []
volume_sc = []
energy_sc = []
fvib_sc = []
helm_sc = [] 		#constant press
helm_sc_2d = []		# PT - 2D matrix

scEnFile = open("sc/data/en.txt", "r")
for line in scEnFile:
	energy_sc.append(float(line))
scEnFile.close()


scVolumeFile = open("sc/data/vol.txt")
for line in scVolumeFile:
	volume_sc.append(float(line))
scVolumeFile.close()

scvibFile = open("sc/data/fvib.txt", "r")

vol_nr = 0
counterr = 0
fvib_sc.append([])
for line in scvibFile:
	if counterr > 101:
		fvib_sc.append([])
		vol_nr += 1
		counterr = 0
	
	fvib_sc[vol_nr].append(float(line))
	counterr += 1
scvibFile.close()

#Data import finished

#Calculate F(T,V):

for i in range(len(energy_sc)):
	helm_sc_2d.append([])
	for j in range (len(fvib_sc[i])):

		helm = 0

		helm = energy_sc[len(energy_sc)-1-i] + fvib_sc[len(energy_sc)-1-i][j]

		helm_sc_2d[i].append(helm)

#print helm_sc_2d
#print energy_sc[0]
#print fvib_sc[0][101]

helmFile_sc = open("sc/data/helm.txt", "w")

for col in range(len(helm_sc_2d)):
	for row in range(len(helm_sc_2d[col])):
		helmFile_sc.write(str(helm_sc_2d[col][row]) + " ")
	helmFile_sc.write("\n")
helmFile_sc.close()

temp = np.array(temp)
vol = np.array(volume_sc)

#create small-to-big volume array
for it in range(len(volume_sc)):
	vol[it] = volume_sc[len(volume_sc)-1-it]



helm_list = np.array(helm_sc_2d)
helm_press_sc = np.array(helm_sc_2d)
#print vol
#print helm_list

sp = interpolate.RectBivariateSpline(vol, temp, helm_list, kx=3 , ky=3 , s = 0)
#Find derivative of F(T,V) dF/dV (const T):

for der in range(len(vol)):
	for dere in range(len(temp)):
		helm_press_sc[der][dere] = sp.__call__(vol[der], temp[dere],mth=None, dx=1, dy=0, grid=False)

#print helm_press_sc

#Calc 2D gibbs
gibbs_sc = []

for i in range(len(helm_press_sc)): #4
	gibbs_sc.append([])
	press_sc.append([])
	press_sc[i] = -1*helm_press_sc[len(helm_press_sc)-1-i][0]
	for j in range (len(helm_press_sc[0])): #102

		gibbs = 0

		gibbs = helm_sc_2d[len(helm_press_sc)-1-i][j] - volume_sc[i]*helm_press_sc[len(helm_press_sc)-1-i][j]

		gibbs_sc[i].append(gibbs)
#print press_sc

print press_sc

gibbs_sc = np.array(gibbs_sc)
press_sc = np.array(press_sc)
press_sc[0] *= 0.0001

cont_gibbs_sc = interpolate.RectBivariateSpline(press_sc, temp, gibbs_sc, kx=3 , ky=3 , s = 0)

#Make contour plot: p3 vs p1
n = 20
x = np.linspace(0, 0.3, n)
y = np.linspace(0, 300, n)
X,Y = np.meshgrid(x, y)

pl.contourf(x, y, cont_gibbs_sc([x],[y]), 20, alpha=.75, cmap=pl.cm.hot)
C = pl.contour(x, y, cont_gibbs_sc([x],[y]), 10, colors='black', linewidth=0.5)
pl.clabel(C, inline=1, fontsize=10)

pl.xticks(())
pl.yticks(())
pl.show()

#Import data: fcc

pt_plot = []
press_fcc = []
volume_fcc = []
energy_fcc = []
fvib_fcc = []
entro_fcc = []
helm_fcc = [] 		#constant press
helm_fcc_2d = []		# PT - 2D matrix

fccEnFile = open("fcc/data/en.txt", "r")
for line in fccEnFile:
	energy_fcc.append(float(line) / 4)
fccEnFile.close()


fccVolumeFile = open("fcc/data/vol.txt")
for line in fccVolumeFile:
	volume_fcc.append(float(line) / 4)
fccVolumeFile.close()

fccEntFile = open("fcc/data/entro.txt", "r")
for line in fccEntFile:
	entro_fcc.append(float(line))
fccEntFile.close()

fccvibFile = open("fcc/data/fvib.txt", "r")

vol_nr = 0
counterr = 0
fvib_fcc.append([])
for line in fccvibFile:
	if counterr > 101:
		fvib_fcc.append([])
		vol_nr += 1
		counterr = 0
	
	fvib_fcc[vol_nr].append(float(line))
	counterr += 1
fccvibFile.close()

#Data import finished

#Calculate F(T,V):

for i in range(len(energy_fcc)):
	helm_fcc_2d.append([])
	for j in range (len(fvib_fcc[i])):

		helm = 0

		helm = energy_fcc[len(energy_fcc)-1-i] + fvib_fcc[len(energy_fcc)-1-i][j]

		helm_fcc_2d[i].append(helm)

#print helm_fcc_2d
#print energy_fcc[0]
#print fvib_fcc[0][101]

helmFile_fcc = open("fcc/data/helm.txt", "w")

for col in range(len(helm_fcc_2d)):
	for row in range(len(helm_fcc_2d[col])):
		helmFile_fcc.write(str(helm_fcc_2d[col][row]) + " ")
	helmFile_fcc.write("\n")
helmFile_fcc.close()

temp = np.array(temp)
vol = np.array(volume_fcc)

#create small-to-big volume array
for it in range(len(volume_fcc)):
	vol[it] = volume_fcc[len(volume_fcc)-1-it]



helm_list = np.array(helm_fcc_2d)
#print vol
#print helm_list

sp = interpolate.RectBivariateSpline(vol, temp, helm_list, kx=3 , ky=3 , s = 0)
#Find derivative of F(T,V) dF/dV (const T):
helm_press_fcc = sp.__call__(vol, temp,mth=None, dx=1, dy=0, grid=True)

#print helm_press_fcc

#Calc 2D gibbs
gibbs_fcc = []

for i in range(len(helm_press_fcc)): #4
	gibbs_fcc.append([])
	press_fcc.append([])
	press_fcc[i] = -1*helm_press_fcc[len(helm_press_fcc)-1-i][0]
	for j in range (len(helm_press_fcc[0])): #102

		gibbs = 0

		gibbs = helm_fcc_2d[len(helm_press_fcc)-1-i][j] - volume_fcc[i]*helm_press_fcc[len(helm_press_fcc)-1-i][j]

		gibbs_fcc[i].append(gibbs)
#print press_fcc

print press_fcc

gibbs_fcc = np.array(gibbs_fcc)
press_fcc = np.array(press_fcc)
press_fcc[0] *= 0.0001

cont_gibbs_fcc = interpolate.RectBivariateSpline(press_fcc, temp, gibbs_fcc, kx=3 , ky=3 , s = 0)

#Make contour plot: p3 vs p1
n = 20
x = np.linspace(0, 0.3, n)
y = np.linspace(0, 300, n)
X,Y = np.meshgrid(x, y)

pl.contourf(x, y, cont_gibbs_fcc([x],[y]), 20, alpha=.75, cmap=pl.cm.hot)
C = pl.contour(x, y, cont_gibbs_fcc([x],[y]), 10, colors='black', linewidth=0.5)
pl.clabel(C, inline=1, fontsize=10)

pl.xticks(())
pl.yticks(())
pl.show()

#Import data: bcc

pt_plot = []
press_bcc = []
volume_bcc = []
energy_bcc = []
fvib_bcc = []
entro_bcc = []
helm_bcc = [] 		#constant press
helm_bcc_2d = []		# PT - 2D matrix

bccEnFile = open("bcc/data/en.txt", "r")
for line in bccEnFile:
	energy_bcc.append(float(line) / 2)
bccEnFile.close()


bccVolumeFile = open("bcc/data/vol.txt")
for line in bccVolumeFile:
	volume_bcc.append(float(line) / 2)
bccVolumeFile.close()

bccEntFile = open("bcc/data/entro.txt", "r")
for line in bccEntFile:
	entro_bcc.append(float(line))
bccEntFile.close()

bccvibFile = open("bcc/data/fvib.txt", "r")

vol_nr = 0
counterr = 0
fvib_bcc.append([])
for line in bccvibFile:
	if counterr > 101:
		fvib_bcc.append([])
		vol_nr += 1
		counterr = 0
	
	fvib_bcc[vol_nr].append(float(line))
	counterr += 1
bccvibFile.close()

#Data import finished

#Calculate F(T,V):

for i in range(len(energy_bcc)):
	helm_bcc_2d.append([])
	for j in range (len(fvib_bcc[i])):

		helm = 0

		helm = energy_bcc[len(energy_bcc)-1-i] + fvib_bcc[len(energy_bcc)-1-i][j]

		helm_bcc_2d[i].append(helm)

#print helm_bcc_2d
#print energy_bcc[0]
#print fvib_bcc[0][101]

helmFile_bcc = open("bcc/data/helm.txt", "w")

for col in range(len(helm_bcc_2d)):
	for row in range(len(helm_bcc_2d[col])):
		helmFile_bcc.write(str(helm_bcc_2d[col][row]) + " ")
	helmFile_bcc.write("\n")
helmFile_bcc.close()

temp = np.array(temp)
vol = np.array(volume_bcc)

#create small-to-big volume array
for it in range(len(volume_bcc)):
	vol[it] = volume_bcc[len(volume_bcc)-1-it]



helm_list = np.array(helm_bcc_2d)
#print vol
#print helm_list

sp = interpolate.RectBivariateSpline(vol, temp, helm_list, kx=3 , ky=3 , s = 0)
#Find derivative of F(T,V) dF/dV (const T):
helm_press_bcc = sp.__call__(vol, temp,mth=None, dx=1, dy=0, grid=True)

#print helm_press_bcc

#Calc 2D gibbs
gibbs_bcc = []

for i in range(len(helm_press_bcc)): #4
	gibbs_bcc.append([])
	press_bcc.append([])
	press_bcc[i] = -1*helm_press_bcc[len(helm_press_bcc)-1-i][0]
	for j in range (len(helm_press_bcc[0])): #102

		gibbs = 0

		gibbs = (helm_bcc_2d[len(helm_press_bcc)-1-i][j] - volume_bcc[i]*helm_press_bcc[len(helm_press_bcc)-1-i][j])

		gibbs_bcc[i].append(gibbs)
#print press_bcc

print press_bcc

gibbs_bcc = np.array(gibbs_bcc)
press_bcc = np.array(press_bcc)
press_bcc[0] *= 0.3

cont_gibbs_bcc = interpolate.RectBivariateSpline(press_bcc, temp, gibbs_bcc, kx=3 , ky=3 , s = 0)

#Make contour plot: p3 vs p1
n = 20
x = np.linspace(0, 0.3, n)
y = np.linspace(0, 300, n)
X,Y = np.meshgrid(x, y)

pl.contourf(x, y, cont_gibbs_bcc([x],[y]), 20, alpha=.75, cmap=pl.cm.hot)
C = pl.contour(x, y, cont_gibbs_bcc([x],[y]), 10, colors='black', linewidth=0.5)
pl.clabel(C, inline=1, fontsize=10)

pl.xticks(())
pl.yticks(())
pl.show()

#Import data: beta

pt_plot = []
press_beta = []
volume_beta = []
energy_beta = []
fvib_beta = []
entro_beta = []
helm_beta = [] 		#constant press
helm_beta_2d = []		# PT - 2D matrix

betaEnFile = open("beta/data/en.txt", "r")
for line in betaEnFile:
	energy_beta.append(float(line) / 4)
betaEnFile.close()


betaVolumeFile = open("beta/data/vol.txt")
for line in betaVolumeFile:
	volume_beta.append(float(line) / 4)
betaVolumeFile.close()

betaEntFile = open("beta/data/entro.txt", "r")
for line in betaEntFile:
	entro_beta.append(float(line))
betaEntFile.close()

betavibFile = open("beta/data/fvib.txt", "r")

vol_nr = 0
counterr = 0
fvib_beta.append([])
for line in betavibFile:
	if counterr > 101:
		fvib_beta.append([])
		vol_nr += 1
		counterr = 0
	
	fvib_beta[vol_nr].append(float(line))
	counterr += 1
betavibFile.close()

#Data import finished

#Calculate F(T,V):

for i in range(len(energy_beta)):
	helm_beta_2d.append([])
	for j in range (len(fvib_beta[i])):

		helm = 0

		helm = energy_beta[len(energy_beta)-1-i] + fvib_beta[len(energy_beta)-1-i][j]

		helm_beta_2d[i].append(helm)

#print helm_beta_2d
#print energy_beta[0]
#print fvib_beta[0][101]

helmFile_beta = open("beta/data/helm.txt", "w")

for col in range(len(helm_beta_2d)):
	for row in range(len(helm_beta_2d[col])):
		helmFile_beta.write(str(helm_beta_2d[col][row]) + " ")
	helmFile_beta.write("\n")
helmFile_beta.close()

temp = np.array(temp)
vol = np.array(volume_beta)

#create small-to-big volume array
for it in range(len(volume_beta)):
	vol[it] = volume_beta[len(volume_beta)-1-it]



helm_list = np.array(helm_beta_2d)
#print vol
#print helm_list

sp = interpolate.RectBivariateSpline(vol, temp, helm_list, kx=3 , ky=3 , s = 0)
#Find derivative of F(T,V) dF/dV (const T):
helm_press_beta = sp.__call__(vol, temp,mth=None, dx=1, dy=0, grid=True)

#print helm_press_beta

#Calc 2D gibbs
gibbs_beta = []

for i in range(len(helm_press_beta)): #4
	gibbs_beta.append([])
	press_beta.append([])
	press_beta[i] = -1*helm_press_beta[len(helm_press_beta)-1-i][0]
	for j in range (len(helm_press_beta[0])): #102

		gibbs = 0

		gibbs = helm_beta_2d[len(helm_press_beta)-1-i][j] - volume_beta[i]*helm_press_beta[len(helm_press_beta)-1-i][j]

		gibbs_beta[i].append(gibbs)
#print press_beta

print press_beta

gibbs_beta = np.array(gibbs_beta)
press_beta = np.array(press_beta)
press_beta[0] *= 0.0001

cont_gibbs_beta = interpolate.RectBivariateSpline(press_beta, temp, gibbs_beta, kx=3 , ky=3 , s = 0)

#Make contour plot: p3 vs p1
n = 20
x = np.linspace(0, 0.3, n)
y = np.linspace(0, 300, n)


pl.contourf(x, y, cont_gibbs_beta([x],[y]), 20, alpha=.75, cmap=pl.cm.hot)
C = pl.contour(x, y, cont_gibbs_beta([x],[y]), 10, colors='black', linewidth=0.5)
pl.clabel(C, inline=1, fontsize=10)

pl.xticks(())
pl.yticks(())
pl.show()

fig = plt.figure()
ax = fig.gca(projection='3d')

n = 50
x = np.linspace(0, 0.16, n)
y = np.linspace(0, 300, n)
X,Y = np.meshgrid(x, y)
#z = cont_gibbs_sc([x],[y])
#zz = cont_gibbs_bcc([x],[y])
#zzz = cont_gibbs_fcc([x],[y])
#zzzz = cont_gibbs_beta([x],[y])
z = cont_gibbs_sc([x],[y])
zz = cont_gibbs_bcc([x],[y])
zzz = cont_gibbs_fcc([x],[y])
zzzz = cont_gibbs_beta([x],[y])
ax.plot_surface(X,Y,z, rstride=1, cstride=1, color='b', antialiased=False)
ax.plot_surface(X,Y,zz, rstride=1, cstride=1, color='r', antialiased=False)
ax.plot_surface(X,Y,zzz, rstride=1, cstride=1, color='g', antialiased=False)
ax.plot_surface(X,Y,zzzz, rstride=1, cstride=1, color='y', antialiased=False)
plt.show()

