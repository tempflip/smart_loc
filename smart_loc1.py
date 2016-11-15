import ip_webcam
import json
import time

cam = ip_webcam.ip_webcam(endpoint = 'http://192.168.0.190:8080/sensors.json')


#print cam.desc_sense('gyro')


THR = 0.01
g = 0
dt = 0
timestamp = 0
while True:
	d = cam.sense_once('gyro')
	v = d[1]
	
	last_timestamp = timestamp
	timestamp = d[0]

	dt = timestamp - last_timestamp

	#print timestamp, last_timestamp, dt

	if (abs(v[1]) < THR) : continue
	g += v[1] #* dt
	
	print dt, v[1], g

	#print time.strftime("%a %d %b %Y %H:%M:%S GMT", time.localtime(timestamp / 1000.0)),
	#print '#', v[1], dt
	#print g, 




