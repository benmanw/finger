import SimpleCV

display = SimpleCV.Display()
cam = SimpleCV.Camera()


while display.isNotDone():
	img = cam.getImage()
	fs = img.findSkintoneBlobs()
	if( fs is not None ):
		fs.draw()