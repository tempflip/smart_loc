import ip_webcam
import time
from math import *

TO_DEG = 57.2958

webcam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=['gyro', 'rot_vector'])

def quaternion_to_eulerian_angle(x,y,z,w):
	ysqr = y * y

	# roll -> x
	t0 = 2. * (w * x + y * z)
	t1 = 1. - 2. * (x * x + ysqr)
	roll = atan2(t0, t1)

	# pitch -> y
	t2 = 2. * (w * y - z * x);
	
	if t2 > 1. : t2 = 1
	if t2 < -1.: t2 = -1.
	pitch = asin(t2)
	
	# yaw -> z
	t3 = 2. * (w * z + x * y);
	t4 = 1. - 2. * (ysqr + z * z);  
	yaw = atan2(t3, t4);

	return roll, pitch, yaw

while True:
	webcam.sense_async()

	if webcam.sense_avail():
		sense = webcam.sense_pop()

		(timestamp, (x_sin, y_sin, z_sin, cos_theta, accuracy)) = sense['rot_vector']

		#print x_sin, y_sin, z_sin, cos_theta

		((axis_x, axis_y, axis_z), alpha) = ip_webcam.calc_rot(x_sin, y_sin, z_sin, cos_theta)

		ra, rb = ip_webcam.rot_axis_to_angle(axis_x, axis_y, axis_z)


		#print "x: {}, y: {}, z: {}, \t\t alpha: {}".format(int(axis_x * 100), int(axis_y * 100) , int(axis_z * 100), alpha * TO_DEG)
		#print ra * TO_DEG, rb * TO_DEG
		roll_, pitch_, yaw_ = quaternion_to_eulerian_angle(x_sin, y_sin, z_sin, cos_theta)







""""


static void toEulerianAngle(const Quaterniond& q, double& roll, double& pitch, double& yaw)
{
	double ysqr = q.y() * q.y();

	// roll (x-axis rotation)
	double t0 = +2.0f * (q.w() * q.x() + q.y() * q.z());
	double t1 = +1.0f - 2.0f * (q.x() * q.x() + ysqr);
	roll = std::atan2(t0, t1);

	// pitch (y-axis rotation)
	double t2 = +2.0f * (q.w() * q.y() - q.z() * q.x());
	t2 = t2 > 1.0f ? 1.0f : t2;
	t2 = t2 < -1.0f ? -1.0f : t2;
	pitch = std::asin(t2);

	// yaw (z-axis rotation)
	double t3 = +2.0f * (q.w() * q.z() + q.x() *q.y());
	double t4 = +1.0f - 2.0f * (ysqr + q.z() * q.z());  
	yaw = std::atan2(t3, t4);
}

"""