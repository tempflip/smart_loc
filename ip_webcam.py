import requests
from requests_futures.sessions import FuturesSession
import unirest
import math
import cv2
import numpy as np
import time
import copy


class ip_webcam:
	def __init__(self, endpoint = 'http://192.168.0.190:8080/sensors.json', sense = [], max_callouts_per_sec = 5, all_points=False):
		self.endpoint = endpoint + '?sense=' + ','.join(sense)
		self.sense_stack = []
		self.sense = sense
		self.use_as_camera = False
		self.photo = None
		self.max_callouts_per_sec = max_callouts_per_sec
		self.last_callout = time.time()
		self.all_points = all_points
		self.timestamp_map = {}
		self._timestamp_map = {}

		if ('photo' in sense):
			self.use_as_camera = True

	def sense_async(self):
		if (time.time() - self.last_callout) < (1. / self.max_callouts_per_sec): return
		self.last_callout = time.time()

		callback = self.result_callback
		if (self.use_as_camera == True):
			callback = self.photo_callback

		unirest.get(self.endpoint, callback = callback)

	def result_callback(self, r):
		# adding the last sense data for every sense
		sense_map = {}
		for s in self.sense:
			sense_map[s] = r.body[s]['data'][-1]

			if self.all_points == True:
				if s not in self.timestamp_map: self.timestamp_map[s] = {}
				for point in r.body[s]['data']:
					self.timestamp_map[s][point[0]] = point[1]
		
		self.sense_stack.append(sense_map)
		self._timestamp_map = copy.deepcopy(self.timestamp_map)

	def sense_avail(self):
		return len(self.sense_stack) > 0

	def sense_pop(self):
		return self.sense_stack.pop()


	def photo_callback(self, r):
		arr = np.asarray(bytearray(r.raw_body), dtype=np.uint8)
		img = cv2.imdecode(arr,-1)
		self.photo = img

	def photo_available(self):
		return self.photo != None

	def get_time_points(self, key):
		if key in self._timestamp_map:
			points = []
			for k in self._timestamp_map[key]:
				points.append([k, self._timestamp_map[key][k][0], self._timestamp_map[key][k][1], self._timestamp_map[key][k][2]])
				points.sort(key=lambda x:x[0])
			return points[-100:]
		else: return []


#### DEPRECATED
# returns (rotation_axis, rot_angle)
def calc_rot(x, y, z, w):
	# x = rotationAxisX * sin(rot_angle / 2)
	# y = rotationAxisY * sin(rot_angle / 2)
	# z = rotationAxisZ * sin(rot_angle / 2)
	# w = cos(rot_angle / 2)

	# -> rot_angle / 2 = acos(w)
	# -> M = sin(rot_angle / 2)

	# M - a constant which is plugged into x, y, z

	theta_per_2 = math.acos(w)
	M = math.sin(theta_per_2)

	# rot_axis_x = x / sin(rot_angle / 2)
	# -> rot_axis_x = x / M
	if M != 0 : 
		rot_axis_x = x / M
		rot_axis_y = y / M
		rot_axis_z = z / M
	else :
		rot_axis_x = 0
		rot_axis_y = 0
		rot_axis_z = 0


	return (rot_axis_x, rot_axis_y, rot_axis_z), theta_per_2 * 2


#### DEPRECATED
# turns a 3d vector to 2 angles: (alpha, beta)
def rot_axis_to_angle(x, y, z):
	""" the math:
	http://stackoverflow.com/questions/30011741/3d-vector-defined-by-2-angles
	x = cos(alpha) * cos(beta);
	z = sin(alpha) * cos(beta);
	y = sin(beta);
	

	###
	### NEED TO BE NORMALIZED !!!!!
	### sqrt(x ** 2 + y ** 2 + z **2) == 1

	"""

	norm_val = math.sqrt(x**2 + y**2 + z**2)
	x = x / norm_val
	y = y / norm_val
	z = z / norm_val

	beta = math.asin(y)
	alpha = math.acos( x / math.cos(beta))
	return alpha, beta


def quaternion_to_eulerian_angle(x,y,z,w):
	ysqr = y * y

	# roll -> x
	t0 = 2. * (w * x + y * z)
	t1 = 1. - 2. * (x * x + ysqr)
	roll = math.atan2(t0, t1)

	# pitch -> y
	t2 = 2. * (w * y - z * x);
	
	if t2 > 1. : t2 = 1
	if t2 < -1.: t2 = -1.
	pitch = math.asin(t2)
	
	# yaw -> z
	t3 = 2. * (w * z + x * y);
	t4 = 1. - 2. * (ysqr + z * z);  
	yaw = math.atan2(t3, t4);

	return roll, pitch, yaw












