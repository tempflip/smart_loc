import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

m = np.loadtxt("md_data.csv")
m = np.transpose(m)

#print np.corrcoef(m)

print m[2].shape

poly = PolynomialFeatures(degree = 2)
train_poly = poly.fit_transform(m[2])

print train_poly.shape
exit()

regr = linear_model.LinearRegression()
regr.fit(m[2].reshape(m[2].shape[0], 1), m[3])


y = [regr.predict(x)[0] for x in range(360)]

print y

plt.subplot(3, 1, 1)
plt.scatter(m[2], m[3])
plt.subplot(3, 1, 2)
plt.scatter(m[2], m[4])
plt.subplot(3, 1, 3)
plt.scatter(range(360), y)

plt.show()

