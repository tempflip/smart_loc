from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam

FPS = 50
WIN_WIDTH = 500
WIN_HEIGHT = 500
WHITE = (255, 255, 255)

g = PlaneGroup();

for n in range(3):
	plane1 = Plane([P3d(10,10,40 * n), P3d(300,10,40 * n), P3d(300,300,40 * n), P3d(10,300,40 * n)])
	g.add_plane(plane1)




def run():
	pygame.init()

	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	pygame.display.set_caption("Wooo Hoooo")

	webcam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=['gyro', 'rot_vector'])
	ticker = 0
	sense_per_sec = 2

	center = (200, 200, 200)

	vx = 100
	vy = 150
	vz = 100

	ra = math.pi
	rb = math.pi
	rg = math.pi

	roll = 0
	pitch = 0
	yaw = 0


	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		keys = pygame.key.get_pressed()
		
		if keys[K_DOWN] :
			vy += 1

		if keys[K_UP] :
			vy -= 1

		if keys[K_LEFT] :
			vx += 1

		if keys[K_RIGHT] :
			vx -= 1

		if keys[K_m] :
			vz += 1

		if keys[K_n] :
			vz -= 1

		if keys[K_a] :
			g.rot(center, -pi / 100, 0, 0)

		if keys[K_d] :
			g.rot(center, pi / 100, 0, 0)

		if keys[K_w] :
			g.rot(center, 0, -pi / 100, 0)

		if keys[K_s] :
			g.rot(center, 0, pi / 100, 0)

		if keys[K_z] :
			g.rot(center, 0, 0, -pi / 100)

		if keys[K_c] :
			g.rot(center, 0, 0, pi / 100)

		if keys[K_SPACE] :
			pass

		ticker = (ticker + 1) % FPS

		webcam.sense_async()

		if webcam.sense_avail():
			sense = webcam.sense_pop()	

			(timestamp, (x_sin, y_sin, z_sin, cos_theta, accuracy)) = sense['rot_vector']
			roll_, pitch_, yaw_ = ip_webcam.quaternion_to_eulerian_angle(x_sin, y_sin, z_sin, cos_theta)


			if roll_ != roll or pitch_ != pitch or yaw_ != yaw :
				d_roll = roll_ - roll
				d_pitch = pitch_ - pitch
				d_yaw = yaw_ - yaw
				print d_roll * TO_DEG, d_pitch * TO_DEG, d_yaw * TO_DEG

				roll = roll_
				pitch = pitch_
				yaw = yaw_

				g.rot(center, 0,0, d_roll)
				g.rot(center, d_pitch, 0, 0)
				g.rot(center, 0, d_yaw, 0)


		clock.tick(FPS)
	

		screen.fill((0,0,0))

		g.draw(screen, viewer_pos=(vx, vy, vz))


		pygame.display.flip()



if __name__ == '__main__':
	run()