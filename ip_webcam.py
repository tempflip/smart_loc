import requests

ENDPOINT = 'http://192.168.0.190:8080/sensors.json'

class ip_webcam:
	def __init__(self):
		pass

	def get_sensors(self, sense=[]):
		url = ENDPOINT + '?sense=' + ','.join(sense)
		r = requests.get(url)
		return r.json()

	def desc_sense(self, sense):
		d = self.get_sensors(sense=[sense])
		return d[sense]['desc']

	def sense_once(self, sense):
		d = self.get_sensors(sense=[sense])
		return d[sense]['data'][-1]



