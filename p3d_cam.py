from p3d import *
import sys, math, pygame
from pygame.locals import *
import ip_webcam

TO_DEG = 57.2958

FPS = 20
WIN_WIDTH = 500
WIN_HEIGHT = 500
WHITE = (255, 255, 255)
RED = (255, 0, 0)
center = (250, 250, 250)
cam_pos = (250, 250, 200)

cam_plane_init = [
	P3d(x=100, y = 100, z = 500),
	P3d(x=500, y = 100, z = 500),
	P3d(x=500, y = 500, z = 500),
	P3d(x=100, y = 500, z = 500)
]


def run():
	pygame.init()
	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()
	pygame.display.set_caption("Wooo Hoooo")

	pt_center = P3d(x=center[0], y=center[1], z=center[2])

	cam_plane = Plane(cam_plane_init)

	img = Img('pusheen.png', w=100, h=100)

 	cam = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/sensors.json', sense=['gyro', 'rot_vector', 'mag'])

	photo = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/photo.jpg', sense=['photo'])

	photo_ticker = 0

	#img_dest_list = []

	rot_last = None

	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		## keys

		keys = pygame.key.get_pressed()

		if keys[K_a] :
			cam_plane.rot(center, 0, -pi / 100, 0)

		if keys[K_d] :
			cam_plane.rot(center, 0, +pi / 100, 0)

		if keys[K_SPACE] :
			#img_dest_list.append(cam_plane.get_points(viewer_pos=cam_pos))
			print "alpha: {} beta: {} angle: {}".format(alpha * TO_DEG, beta * TO_DEG, angle * TO_DEG)
			pass

		clock.tick(FPS)
		photo_ticker = (photo_ticker + 1) % (FPS / 2) 

		## sense
		cam.sense_async()

		if photo_ticker == 0:
			photo.sense_async()

		if cam.sense_avail():
			sense = cam.sense_pop()
			#rot_x, rot_y, rot_z, rot_cos, acc = sense['rot_vector'][1]
			#rot_axis, angle = ip_webcam.calc_rot(rot_x, rot_y, rot_z, rot_cos)
			#(alpha, beta) = ip_webcam.rot_axis_to_angle(rot_axis[0], rot_axis[1], rot_axis[2])

			#print "rot_axis: {} angle : {}".format(rot_axis, angle * TO_DEG)
			#print "alpha: {} beta: {} angle: {}".format(alpha, beta, angle)




			if (rot_last != None):
				(alpha_last, beta_last, angle_last) = rot_last
				alpha_d = alpha - alpha_last
				beta_d = beta - beta_last
				angle_d = angle - angle_last

				cam_plane.rot(center, 0, angle_d, 0)
				#cam_plane.rot(center, beta_d, 0, 0)
				#cam_plane.rot(center, 0, 0, alpha_d)

			rot_last = (alpha, beta, angle)




		## draw
		#############
		screen.fill((0,0,0))


		pt_center_2d = pt_center.proj_2d(viewer_pos=cam_pos)

		cam_plane.draw(screen, viewer_pos=cam_pos)

		if photo.photo_available() :
			#photo_image = Img(img_array=photo.photo)
			#photo_image.draw2(screen, cam_plane.get_points(viewer_pos=cam_pos))
			pass
		#img.draw2(screen, cam_plane.get_points(viewer_pos=cam_pos))

		#for dest in img_dest_list:
		#	img.draw2(screen, dest)

		pygame.display.flip()				



if __name__ == "__main__":
	run()
