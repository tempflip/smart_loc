from math import *
import pygame
import numpy as np

TO_DEG = 57.2958

class P3d:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x, self.y, self.z = x, y, z

	def __str__(self):
		return "p3d point x: {} y: {} z: {}".format(self.x, self.y, self.z)

	def set_coord(self, x, y, z):
		self.x, self.y, self.z = x, y, z

	# window x, window y
	def proj_2d(self, viewer_pos = (150, 150, 100)):
		viewer_z = viewer_pos[2]
		prop = self.z + viewer_z


		calc_x = abs(viewer_pos[0] - self.x)
		calc_y = abs(viewer_pos[1] - self.y)

		proj_x = (calc_x  * viewer_z) / prop
		proj_y = (calc_y  * viewer_z) / prop

		#adjusting to the window center

		if (self.x >= viewer_pos[0]):
			proj_x = viewer_pos[0] + proj_x
		else :
			proj_x = viewer_pos[0] - proj_x

		if (self.y >= viewer_pos[1]):
			proj_y = viewer_pos[1] + proj_y
		else :
			proj_y = viewer_pos[1] - proj_y

		return (proj_x, proj_y)


class Plane():
	def __init__(self, point_list=[]):
		self.point_list = point_list

	def rot(self, center, a):

		m_a = np.array([[cos(a), -sin(a)], [sin(a), cos(a)]])

		for p in self.point_list:
			coord = np.dot(m_a, np.array([[p.x], [p.y]]) )
			p.set_coord(coord[0][0], coord[1][0], p.z)



	def draw(self, pygame_display, color = (255, 255, 255), viewer_pos=(150, 150, 100)):
		for i in range(len(self.point_list) - 1):
			pygame.draw.line(pygame_display, color, self.point_list[i].proj_2d(viewer_pos=viewer_pos), self.point_list[i+1].proj_2d(viewer_pos=viewer_pos))
		pygame.draw.line(pygame_display, color, self.point_list[-1].proj_2d(viewer_pos=viewer_pos), self.point_list[0].proj_2d(viewer_pos=viewer_pos))

	def print_out(self):
		for p in self.point_list:
			print p


class PlaneGroup():
	def __init__(self, plane_list=[]):
		self.plane_list = plane_list

	def add_plane(self, plane):
		self.plane_list.append(plane)

	def draw(self, display, viewer_pos):
		for plane in self.plane_list:
			plane.draw(display, viewer_pos = viewer_pos)

	def rot(self, center, a):
		for plane in self.plane_list:
			plane.rot(center, a)
