import ip_webcam
import matplotlib.pyplot as plt
import cv2

photo = ip_webcam.ip_webcam(endpoint = 'http://192.168.1.102:8080/photo.jpg', sense=['photo'])
photo.sense_async()


while 1:
	if photo.photo_available():
		photo = cv2.cvtColor(photo.photo, cv2.COLOR_BGR2GRAY)
		photo = cv2.resize((photo / 20) * 20, (100, 100))
		break


print photo.shape
plt.imshow(photo)
plt.show()