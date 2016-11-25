from p3d import *
import sys, math, pygame
from pygame.locals import *


FPS = 50
WIN_WIDTH = 500
WIN_HEIGHT = 500
WHITE = (255, 255, 255)

g = PlaneGroup();

for n in range(10):
	plane1 = Plane([P3d(10,10,40 * n), P3d(300,10,40 * n), P3d(300,300,40 * n), P3d(10,300,40 * n)])
	g.add_plane(plane1)


def run():
	pygame.init()

	screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	pygame.display.set_caption("Wooo Hoooo")


	center = (200, 200, 200)

	vx = 100
	vy = 150
	vz = 100

	ra = math.pi
	rb = math.pi
	rg = math.pi

	rl, rr = False, False

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
			g.rot(center, -pi / 100)

		if keys[K_d] :
			g.rot(center, pi / 100)

		if keys[K_SPACE] :
			pass



		clock.tick(FPS)
		screen.fill((0,0,0))

		g.draw(screen, viewer_pos=(vx, vy, vz))


		pygame.display.flip()




if __name__ == '__main__':
	run()