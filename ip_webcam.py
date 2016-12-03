import requests
from requests_futures.sessions import FuturesSession
import unirest
import math
import cv2
import numpy as np



class ip_webcam:
	def __init__(self, endpoint = 'http://192.168.0.190:8080/sensors.json', sense = []):
		self.endpoint = endpoint + '?sense=' + ','.join(sense)
		self.sense_stack = []
		self.sense = sense
		self.use_as_camera = False
		self.photo = None

		if ('photo' in sense):
			self.use_as_camera = True

	def sense_async(self):
		callback = self.result_callback
		if (self.use_as_camera == True):
			callback = self.photo_callback

		unirest.get(self.endpoint, callback = callback)

	def result_callback(self, r):
		# adding the last sense data for every sense
		sense_map = {}
		for s in self.sense:
			sense_map[s] = r.body[s]['data'][-1]
		
		self.sense_stack.append(sense_map)

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

	
"""
	
	def get_sensors(self, sense=[]):
		url = self.endpoint + '?sense=' + ','.join(sense)
		print url
		r = requests.get(url)
		return r.json()

	def desc_sense(self, sense):
		d = self.get_sensors(sense=[sense])
		return d[sense]['desc']

	def sense_once(self, sense):
		d = self.get_sensors(sense=[sense])
		return d[sense]['data'][-1]

"""