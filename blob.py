import SimpleCV, math
from time import time

display = SimpleCV.Display()
cam = SimpleCV.Camera()
normaldisplay = True

# Settings
blob_min, blob_max = 5000, 100000

def getPalette(img):
	arr = []
	for x in range(0, img.width, 5):
		for y in range(0, img.height, 5):
			p = list(img.getPixel(x, y))
			for i, val in enumerate(p):
				p[i] = val - val % 5
			arr.append(tuple(p))
	return list(set(arr))

# Calibration
# blob_color = SimpleCV.Color.YELLOW

seconds = 5

start = time()
while time() - start < seconds:
	img = cam.getImage().flipHorizontal()
	countdown = '%s' % (seconds - math.floor(time() - start))
	fontsize = 100
	img.drawText(text=countdown, x=img.width/2-fontsize/2, y=100, color=(0, 255, 0), fontsize=fontsize)
	# img.drawCircle((img.width/2,img.height/2),25,(0,255,0),3)
	img.drawRectangle(img.width/2-50, img.height/2-50, 100, 100, (0, 255, 0), 3)
	img.show()

img = cam.getImage().flipHorizontal()
img.crop(img.width/2-50, img.height/2-50, 100, 100)
#img.palettize()
blob_color = map(int, img.crop(img.width/2-50, img.height/2-50, 100, 100).meanColor())
# blob_palette = getPalette(img)

while display.isNotDone():

	img = cam.getImage().flipHorizontal()

	# Blobs
	#dist = img.edges(t1=160)
	dist = img.dilate(1).colorDistance(blob_color).invert()
	blobbed_image = dist.stretch(200,255)
	#blobbed_image = img.dilate(1).invert().stretch(200,255)
	#blob_palette = img.palettize()
	#blobs = blobbed_image.findBlobs()
	blobs = blobbed_image.findBlobs()
	if blobs:
		big_blobs = [blob for blob in blobs if blob_min < blob.area() < blob_max]
		for blob in big_blobs:
			#blob.draw()
			# blob.centroid()
			blobbed_image.drawCircle(blob.centroid(), 10, color=(255, 255, 0), thickness=-1)
			blob.drawMinRect(img.dl(),(0,255,0),3)
			# blob.

	# Display
	#edged_image.show()
	blobbed_image.show()
	# img.show()

