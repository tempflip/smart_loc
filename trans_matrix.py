import numpy as np 
from p3d import *



a = np.array([[4,5,8],[2,6,5],[1,1,1]])
b = np.array([[5,6,9],[3,7,6],[1,1,1]])


print a

print b

M = calc_trans_matrix(a,b)

print M

print "........"

print np.dot(a, M)