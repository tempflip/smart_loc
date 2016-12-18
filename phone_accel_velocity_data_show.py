from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam
import numpy as np
import copy

def dx(v0, t, a):
	dx = v0 * t + (a * t**2) / 2
	return dx

def v(v0, t, a):
	v = v0 * 0.70  + a * t
	return v

def calculate_velocity(cols):
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

	return vx1, vx2, vx3

webcam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=["lin_accel", "rot_vector"], all_points=True)

while 1:
	webcam.sense_async()

	if webcam.sense_avail():

		d = np.array(webcam.get_time_points('lin_accel'))
		if len(d) == 0: continue

		cols = np.transpose(d)
		cols[3] = cols[3] - 0.65


		vx1, vx2, vx3 = calculate_velocity(cols)

		print "{} \t {} \t {}".format(int(vx1[-1] * 100), int(vx2[-1] * 100), int(vx3[-1] * 100))



