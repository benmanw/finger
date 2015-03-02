import SimpleCV

from SimpleCV import Color, Camera, Display
from itertools import chain
from time import time
from math import floor

# Settings
blob_min, blob_max = 1000, 100000

getFlippedImage = lambda cam: cam.getImage().flipHorizontal()

def blob_centroids(cam, display):

	# UI Settings
	seconds = 5
	fontsize = 100
	boxsize = 100

	# Calibration
	start = time()
	while time() - start < seconds:
		img = getFlippedImage(cam)
		countdown = '%s' % (seconds - floor(time() - start))
		img.drawText(text=countdown, x=img.width/2-fontsize/2, y=boxsize, color=(0, 255, 0), fontsize=fontsize)
		img.drawRectangle(img.width/2-boxsize/2, img.height/2-boxsize/2, boxsize, boxsize, (0, 255, 0), 3)
		img.show()

	img = cam.getImage().flipHorizontal()
	sample_frame = img.crop(img.width/2-50, img.height/2-50, 100, 100)
	blob_color = map(int, sample_frame.meanColor())
	blob_greyscale = sample_frame.greyscale().meanColor()[0]

	greyscale_tolerance = 15
	stretch_by = (blob_greyscale - greyscale_tolerance, blob_greyscale + greyscale_tolerance)

	prev = cam.getImage().flipHorizontal()

	# Find Centroid
	while display.isNotDone():

		img = getFlippedImage(cam)

		dist = img.colorDistance(blob_color)
		blobbed_image = img.dilate(1).stretch(*stretch_by).binarize(thresh=100).invert()
		blobs = blobbed_image.findBlobs()
		if blobs:
			big_blobs = [blob for blob in blobs if blob_min < blob.area() < blob_max]
			centroids = [blob.centroid() for blob in big_blobs]

			yield centroids

def motion_centroids(cam, display):
	second = getFlippedImage(cam)
	while display.isNotDone():
		first = getFlippedImage(cam)
		diff = second.dilate(8) - first.dilate(8)
		second = first
		diff = diff.binarize(thresh=10).invert()

		blobs = diff.findBlobs()
		if blobs:
			big_blobs = [blob for blob in blobs if blob_min < blob.area() < blob_max]
			centroids = [blob.centroid() for blob in big_blobs]
			
			yield centroids

def corners(cam, display):
	while display.isNotDone():
		yield gradient_norms(cam, display).findCorners()

def gradient_norms(cam, display):
	img = getFlippedImage(cam)
	return img.gaussianBlur().morphGradient().invert().binarize(thresh=240).erode(iterations=1)

if __name__ == '__main__':
	args = (Camera(), Display())

	# Draw blob centroids
	# for centroids in chain(blob_centroids(*args), motion_centroids(*args)):
	# 	img = gradient_norms(*args)
	# 	for c in centroids:
	# 		img.drawCircle(c, 10, color=Color.RED, thickness=-1)
	# 	img.show()

	for corners in corners(*args):
		img = gradient_norms(*args)
		for c in corners:
			img.drawCircle(c, 10, color=Color.RED, thickness=-1)
	 	img.show()


