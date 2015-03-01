import SimpleCV, math, numpy
from time import time

display = SimpleCV.Display()
cam = SimpleCV.Camera()
normaldisplay = True

# Settings
blob_min, blob_max = 1000, 10000

# Calibration
seconds = 5

start = time()
while time() - start < seconds:
	img = cam.getImage().flipHorizontal()
	countdown = '%s' % (seconds - math.floor(time() - start))
	fontsize = 100
	img.drawText(text=countdown, x=img.width/2-fontsize/2, y=100, color=(0, 255, 0), fontsize=fontsize)
	img.drawRectangle(img.width/2-50, img.height/2-50, 100, 100, (0, 255, 0), 3)
	img.show()

img = cam.getImage().flipHorizontal()
blob_color = map(int, img.crop(img.width/2-50, img.height/2-50, 100, 100).meanColor())

prev = cam.getImage().flipHorizontal()

# Find Centroid
while display.isNotDone():

	img = cam.getImage().flipHorizontal()

	dist = img.colorDistance(blob_color)
	blobbed_image = img.dilate(2).stretch(200,255)
	blobs = blobbed_image.findBlobs()
	if blobs:
		big_blobs = [blob for blob in blobs if blob_min < blob.area() < blob_max]
		for blob in big_blobs:
			blobbed_image.drawCircle(blob.centroid(), 10, color=blob_color, thickness=-1)

	blobbed_image.show()

