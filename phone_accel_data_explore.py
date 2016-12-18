import sys, math, pygame
import numpy as np

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import datetime

def dx(v0, t, a):
	dx = v0 * t + (a * t**2) / 2
	return dx

def v(v0, t, a):
	v = v0 * 0.99  + a * t
	return v

m = np.loadtxt('acc_data_lin1.csv', dtype=float)

cols = np.transpose(m)
cols[3] = cols[3] - 0.65



vx1 = []
vx2 = []
vx3 = []

dx1 = []
dx2 = []
dx3 = []


for i, timestamp in enumerate(cols[0]):
	if i != 0:
		dt = (timestamp - cols[0][i-1]) / 1000
		v0_1 = vx1[i-1]
		v0_2 = vx2[i-1]
		v0_3 = vx3[i-1]
	else :
		dt = 0
		v0_1 = 0
		v0_2 = 0
		v0_3 = 0

	vx1.append(v(v0_1, dt, cols[1][i]))
	vx2.append(v(v0_2, dt, cols[2][i]))
	vx3.append(v(v0_3, dt, cols[3][i]))

	dx1.append(dx(v0_1, dt, cols[1][i]))
	dx2.append(dx(v0_2, dt, cols[2][i]))
	dx3.append(dx(v0_3, dt, cols[3][i]))



#line_ax = plt.plot(cols[0], cols[1], color="red")
#line_ay = plt.plot(cols[0], cols[2], color="green")
#line_az = plt.plot(cols[0], cols[3], color="blue")

#line_vx1 = plt.plot(cols[0], vx1, color="pink")
line_vx2 = plt.plot(cols[0], vx2, color="magenta")
#line_vx3 = plt.plot(cols[0], vx3, color="black")

#line_dx1 = plt.plot(cols[0], dx1, color="grey")
line_vx2 = plt.plot(cols[0], dx2, color="cyan")


plt.show()