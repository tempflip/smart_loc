from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam

TO_DEG = 57.2958

fname = "{}.csv".format(sys.argv[1])

sense = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=['gyro', 'rot_vector', 'mag'])

datapoints = []

while 1:
	sense.sense_async()
	if sense.sense_avail():
		sense_d = sense.sense_pop()
		
		#rot_x, rot_y, rot_z, rot_cos, acc = sense_d['rot_vector'][1]
		#rot_axis, angle = ip_webcam.calc_rot(rot_x, rot_y, rot_z, rot_cos)
		#(alpha, beta) = ip_webcam.rot_axis_to_angle(rot_axis[0], rot_axis[1], rot_axis[2])	

		mx, my, mz = sense_d['mag'][1]

		print mx, my, mz
		roll = 0
		pitch = 0
		try :
			yaw = input('Enter current yaw.')
		except :
			print "huuuuu"
			continue

		if yaw == 999: break

		observation = [roll, pitch, yaw, mx, my, mz]

		datapoints.append(observation)


print datapoints


arr = np.array(datapoints)
np.savetxt(fname, arr)

