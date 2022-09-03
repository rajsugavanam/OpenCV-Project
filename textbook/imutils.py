import numpy as np
import cv2 as cv

def translate(image, x, y):
	# matrix for translation shifted x and y
	matrix = np.float32( ([1,0,x], [0,1,y]) )
	shifted = cv.warpAffine(image, matrix, (image.shape[1], image.shape[0]) )
	return shifted

def rotate(image, theta, origin=None, scale=1.0):
	(y, x) = image.shape[:2] # exclude color

	if origin is None:
		origin = (x//2, y//2) # default is image center

	matrix = cv.getRotationMatrix2D(origin, theta, scale)
	rotated = cv.warpAffine(image, matrix, (x, y))
	return rotated

# inter is interpolation
def resize(image, width = None, height = None, inter = cv.INTER_AREA):
	dim = None
	(y, x) = image.shape[:2]

	if width is None and height is None: # no scale factor specified, return unscaled
		return image

	if width is None:
		r = height / float(y) # ratio for height scale
		dim = (int(x*r), height) # proportionally resize

	else:
		r = width / float(x)
		dim = (width, int(y*r))
	
	resized = cv.resize(image, dim, interpolation=inter)