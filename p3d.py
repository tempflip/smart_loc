from math import *
import pygame
import numpy as np
#from scipy import misc
import cv2
import matplotlib.pyplot as plt


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

	def rot(self, center, a, b, g):

		m_a = np.array([[cos(a), -sin(a)], [sin(a), cos(a)]])


		for p in self.point_list:
			norm_x = p.x - center[0]
			norm_y = p.y - center[1]
			norm_z = p.z - center[1]


			coord = np.dot(m_a, np.array([[norm_x], [norm_y]]) )
			p.set_coord(coord[0][0] + center[0], coord[1][0] + center[1], p.z)


	def draw(self, pygame_display, color = (255, 255, 255), viewer_pos=(150, 150, 100)):
		for i in range(len(self.point_list) - 1):
			pygame.draw.line(pygame_display, color, self.point_list[i].proj_2d(viewer_pos=viewer_pos), self.point_list[i+1].proj_2d(viewer_pos=viewer_pos))
		pygame.draw.line(pygame_display, color, self.point_list[-1].proj_2d(viewer_pos=viewer_pos), self.point_list[0].proj_2d(viewer_pos=viewer_pos))

	def print_out(self):
		for p in self.point_list:
			print p

	def get_points(self, viewer_pos=(150, 150, 100)):
		pts = []
		for p in self.point_list:
			pts.append(p.proj_2d(viewer_pos=viewer_pos))
		return pts

class PlaneGroup():
	def __init__(self, plane_list=[]):
		self.plane_list = plane_list

	def add_plane(self, plane):
		self.plane_list.append(plane)

	def draw(self, display, viewer_pos):
		for plane in self.plane_list:
			plane.draw(display, viewer_pos = viewer_pos)

	def rot(self, center, a, b, g):
		for plane in self.plane_list:
			plane.rot(center, a, b, g)

class Img:
	def __init__(self, fname=None, w=200, h=200):
		self.shear_matrix = None
		self.scale_matrix = None
		self.rot_matrix = None
		self.w = w
		self.h = h

		if fname != None:
			self.image = self.get_img(fname)
		self.set_scale(1)
		self.set_shear((0,0))
		self.set_rot(0, (0, 0))
		self.update_trans_matrix()



	def get_img(self, fname):
		self.img = cv2.imread(fname, 0)
		self.img = cv2.resize(self.img, (self.w, self.h))


	# draws the image using the transformation params
	def draw(self, pygame_display):
		row_x = []
		row_y = []
		row_z = [] # this going to be a dummy 1 row
		pix_list = []

		for y, row in  enumerate(self.img):
			for x, pix in enumerate(row):
				row_x.append(x)
				row_y.append(y)
				row_z.append(1)
				pix_list.append(pix)


		img_matrix = np.array([row_x, row_y, row_z])
		img_matrix = np.dot(self.trans_matrix, img_matrix)

		for i, pix in enumerate(pix_list):
			pygame_display.set_at((int(img_matrix[0][i]) + self.center[1], int(img_matrix[1][i]) + self.center[0]), (pix, pix, pix))


	# draws the transferred to the provided points
	# dest : (4,2) numpy list of destination points

	def draw2(self, pygame_display, dest):
		src = np.zeros((4, 2), dtype="float32")
		dst = order_points(dest)

		src[1] = [self.w, 0]
		src[2] = [self.w, self.h]
		src[3] = [0, self.h]

		M = cv2.getPerspectiveTransform(src, dst)

		warped = cv2.warpPerspective(self.img, M, (dst[1][0], dst[2][1]))
		#plt.imshow(warped, interpolation="none")
		#plt.show()
		for y, row  in enumerate(warped):
			for x, pix in enumerate(row):
				if pix == 0 : continue
				pygame_display.set_at((x,y), (pix, pix, pix))

	def set_rot(self, deg, center):
		self.rot = deg
		self.rot_matrix = np.array([[ cos(deg), - sin(deg), 0],
								    [ sin(deg),   cos(deg), 0],
								    [0, 0, 1]])
		self.center = center

		self.update_trans_matrix()

	def set_scale(self, scale):
		self.scale = scale
		self.scale_matrix = np.array([[self.scale, 0          , 0],
									   [     0    , self.scale, 0 ],
									   [0, 0, 1]])

		self.update_trans_matrix()


	def set_shear(self, shear):
		self.shear_x, self.shear_y = shear
		
		self.shear_matrix = np.array([[1,           self.shear_x, 0],
									  [self.shear_y,     1      , 0],
									  [0, 0, 1]])

		self.update_trans_matrix()


	def update_trans_matrix(self):
		if self.shear_matrix == None : return
		if self.scale_matrix == None : return
		if self.rot_matrix == None : return

		self.trans_matrix = np.dot(self.scale_matrix, self.shear_matrix)
		self.trans_matrix = np.dot(self.trans_matrix, self.rot_matrix)
		print "trans_matrix:", self.trans_matrix
		print "inv", np.linalg.inv(self.trans_matrix)

	def set_trans_matrix(self, m):
		self.trans_matrix = np.array(m)


# a helper to order the points clockwise, starting from top left
def order_points(point_list):
	pts = np.array(point_list, dtype="float32")
	r = np.zeros((4,2), dtype="float32")
	sums = pts.sum(axis=1)
	r[0] = pts[np.argmin(sums)]
	r[2] = pts[np.argmax(sums)]

	diffs = np.diff(pts, axis=1)

	r[1] = pts[np.argmin(diffs)]
	r[3] = pts[np.argmax(diffs)]

	return r





# a -> starting position, b -> result position
# returns a transaction matrix M, so a * b = M
def calc_trans_matrix(a, b):
	a = np.array(a)
	b = np.array(b)

	M = np.dot(np.linalg.inv(a), b)

	return M





