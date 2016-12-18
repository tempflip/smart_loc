from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam

FPS = 50
WIN_WIDTH = 800
WIN_HEIGHT = 800
WHITE = (255, 255, 255)


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

	return dx1, dx2, dx3


def run():

	pygame.init()
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()
	pygame.display.set_caption("Wooo Hoooo")

	x, y = 400, 400

	webcam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json'
		, sense=["lin_accel", "rot_vector"]
		, all_points=True
		, max_callouts_per_sec = 3)

	pos_list = []

	SM = 400

	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		webcam.sense_async()

		if webcam.sense_avail():

			## rotation
			sense = webcam.sense_pop()	

			(timestamp, (x_sin, y_sin, z_sin, cos_theta, accuracy)) = sense['rot_vector']
			roll_, pitch_, yaw_ = ip_webcam.quaternion_to_eulerian_angle(x_sin, y_sin, z_sin, cos_theta)	

			print roll_ * TO_DEG, pitch_ * TO_DEG, yaw_	 * TO_DEG

			## acceleration

			d = np.array(webcam.get_time_points('lin_accel'))
			if len(d) != 0:

				cols = np.transpose(d)
				cols[3] = cols[3] - 0.65

				vx, vy, vz = calculate_velocity(cols)

				#print "{} \t {} \t {}".format(int(vx[-1] * 100), int(vy[-1] * 100), int(vz[-1] * 100))

				x += (vx[-1] * cos(yaw_) +  vy[-1] * sin(yaw_)) * SM
				y += (vx[-1] * sin(yaw_) + vy[-1] * cos(yaw_)) * SM




				print x, y
				#y += vy[-1] * SM
				


				pos_list.append((x, y))

		clock.tick(FPS)
		screen.fill((0,0,0))

		for i, pos in enumerate(pos_list[-1000:]):
			if i == 0 :
				ppos = pos
				continue
			pygame.draw.line(screen, WHITE, ppos, pos)
			ppos = pos


		#screen.set_at((x, y), WHITE)
		pygame.display.flip()



if __name__ == "__main__":
	run()