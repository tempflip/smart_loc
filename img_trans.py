from p3d import *
import sys, math, pygame
from pygame.locals import *


FPS = 25
WIN_WIDTH = 500
WIN_HEIGHT = 500
WHITE = (255, 255, 255)

img = Img('pusheen.png')
print img.img
#exit()

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


	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		keys = pygame.key.get_pressed()
		
		if keys[K_DOWN] :
			img.set_scale(img.scale - 0.1)

		if keys[K_UP] :
			img.set_scale(img.scale + 0.1)

		if keys[K_LEFT] :
			img.set_rot(img.rot - pi / 40, center=center)

		if keys[K_RIGHT] :
			img.set_rot(img.rot + pi / 40, center=center)

		if keys[K_m] :
			img.set_shear((img.shear_x + 0.3, img.shear_y))

		if keys[K_n] :
			img.set_shear((img.shear_x - 0.3, img.shear_y))


		if keys[K_b] :
			img.set_shear((img.shear_x, img.shear_y + 0.3))

		if keys[K_v] :
			img.set_shear((img.shear_x, img.shear_y - 0.3))

		if keys[K_SPACE] :
			pass



		clock.tick(FPS)
		screen.fill((0,0,0))
		img.draw(screen)

		pygame.display.flip()




if __name__ == '__main__':
	run()