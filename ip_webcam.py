import requests
from requests_futures.sessions import FuturesSession
import unirest

class ip_webcam:
	def __init__(self, endpoint = 'http://192.168.0.190:8080/sensors.json', sense = []):
		self.endpoint = endpoint + '?sense=' + ','.join(sense)
		self.sense_stack = []
		self.sense = sense

	def sense_async(self):
		unirest.get(self.endpoint, callback = self.result_callback)

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