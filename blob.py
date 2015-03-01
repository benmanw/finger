import SimpleCV, math, numpy
from SimpleCV import Color
from time import time

# Settings
blob_min, blob_max = 1000, 100000

getFlippedImage = lambda cam: cam.getImage().flipHorizontal()

def blob_centroids(cam, display, color):

	# Calibration
	seconds = 5
	start = time()
	while time() - start < seconds:
		img = getFlippedImage(cam)
		countdown = '%s' % (seconds - math.floor(time() - start))
		fontsize = 100
		img.drawText(text=countdown, x=img.width/2-fontsize/2, y=100, color=(0, 255, 0), fontsize=fontsize)
		img.drawRectangle(img.width/2-50, img.height/2-50, 100, 100, (0, 255, 0), 3)
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
			for blob in big_blobs:
				blobbed_image.drawCircle(blob.centroid(), 10, color=color, thickness=-1)

		yield blobbed_image

def motion_centroids(cam, display, color):
	second = getFlippedImage(cam)
	while display.isNotDone():
		first = getFlippedImage(cam)
		diff = second.dilate(8) - first.dilate(8)
		second = first
		diff = diff.binarize(thresh=10).invert()

		blobs = diff.findBlobs()
		if blobs:
			big_blobs = [blob for blob in blobs if blob_min < blob.area() < blob_max]
			for blob in big_blobs:
				diff.drawCircle(blob.centroid(), 10, color=color, thickness=-1)

		yield diff

def gradient_norms(cam, display):
	while display.isNotDone():
		img = getFlippedImage(cam)
		yield img.gaussianBlur().morphGradient().invert().binarize(thresh=240)




if __name__ == '__main__':
	cam, display = SimpleCV.Camera(), SimpleCV.Display()

	for frame in blob_centroids(cam, display, Color.RED):
	 	frame.show()
