from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam
import numpy as np


FNAME = "{}.csv".format(sys.argv[1])

webcam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=["accel", "lin_accel"], all_points=True)

c = 0

while c < 1000:
	webcam.sense_async()

	if webcam.sense_avail():
		c = len(webcam.timestamp_map["lin_accel"].keys())
		print c

data_map = webcam.timestamp_map["lin_accel"]
points = []
for k in data_map:
	points.append([k, data_map[k][0], data_map[k][1], data_map[k][2]])

points.sort(key=lambda x:x[0])

arr = np.array(points)
np.savetxt(FNAME, arr)


