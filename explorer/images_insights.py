import numpy as np
import struct
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import urllib
import cv2
import math
from matplotlib import pyplot as plt


def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image


def image_info(post_id, url):
	img = url_to_image(url)
	img = cv2.resize(img, (500, 500)) 
	arr = np.asarray(img)
	shape = arr.shape
	arr = arr.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
	clusters = 2
	codes, dist = scipy.cluster.vq.kmeans(arr, clusters)
	vces, dist = scipy.cluster.vq.vq(arr, codes)
	counts, bins = scipy.histogram(vces,len(codes))
	index_max = scipy.argmax(counts)
	peak = codes[index_max]
	dominant_color = ''.join(chr(int(c)) for c in peak).encode('utf-8').hex()
	avg_color_per_row = np.average(img, axis=0)
	avg_color = np.average(avg_color_per_row, axis=0)
	format_avg_color = "#{:02x}{:02x}{:02x}".format(math.floor(round(avg_color[2],0)), 
		math.floor(round(avg_color[1],0)), 
		math.floor(round(avg_color[0],0)))
	
	color = ('b','g','r')
	for i,col in enumerate(color):
		histogram = cv2.calcHist([img],[i],None,[256],[0,256])
		plt.plot(histogram,color = col)
		plt.xlim([0,256])
		#cv2.imshow("output", img)
	#plt.show()

	image_dict ={
		'post_id': post_id,
		'peak': peak,
		'dominant_color': dominant_color,
		'format_avg_color': format_avg_color
	}

	return(image_dict)


if __name__ == '__main__':
	image_info("https://www.urbanarts.com.br/imagens/produtos/079232/Detalhes/por-do-sol-no-ceara.jpg")