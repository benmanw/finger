import SimpleCV, math
from time import time

display = SimpleCV.Display()
cam = SimpleCV.Camera()
normaldisplay = True

# Settings
blob_threshhold = 1000

# Calibration
# blob_color = SimpleCV.Color.YELLOW
blob_color = (94, 180, 127)

# start = time()
# while time() - start < 5:
# 	img = cam.getImage().flipHorizontal()
# 	countdown = '%s' % (5 - math.floor(time() - start))
# 	fontsize = 100
# 	img.drawText(text=countdown, x=img.width/2-fontsize/2, y=100, color=(0, 255, 0), fontsize=fontsize)
# 	# img.drawCircle((img.width/2,img.height/2),25,(0,255,0),3)
# 	# img.drawRectangle(img.width/2-, img.height/2-25, 25, 25, (0, 255, 0), 3)
# 	img.show()

# img = cam.getImage().flipHorizontal()
# blob_color = map(int, img.crop(img.width/2-50, img.height/2-50, 100, 100).invert().meanColor())
# print blob_color

while display.isNotDone():

	img = cam.getImage().flipHorizontal()

	# Blobs
	#dist = img.edges(t1=160)
	dist = img.dilate(1).colorDistance(blob_color).invert()
	blobbed_image = dist.stretch(200,255)
	#blobbed_image = img
	blobs = blobbed_image.findBlobs()
	if blobs:
		big_blobs = [blob for blob in blobs if blob.area() > blob_threshhold]
		for blob in big_blobs:
			#blob.draw()
			blob.drawMinRect(img.dl(),(0,255,0),3)

	# Display
	#edged_image.show()

	img.show()

