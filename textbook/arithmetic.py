import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

# instead of 7 bits for numbers and one for sign,
# use 8 for numbers (2^8 = 256, start from 0 = 255)
#* cv caps the value
print("max of 255: {}".format( 
	cv.add(np.uint8([200]), np.uint8([100]))
))

print("min of 0: {}".format( 
	cv.subtract(np.uint8([50]), np.uint8([100]))
))

#* np wraps around
print("wrap around: {}"
	.format(np.uint8([200]) + np.uint8([100]))
)

print("wrap around: {}"
	.format(np.uint8([50]) - np.uint8([100]))
)

matrix = np.ones(image.shape, dtype="uint8") * 100
added = cv.add(image, matrix) # add vector [100, 100, 100] to all color vectors
cv.imshow("Added", added)
cv.waitKey(0)

matrix = np.ones(image.shape, dtype="uint8") * 50
added = cv.subtract(image, matrix) # subtract vector [100, 100, 100] to all color vectors
cv.imshow("Subtracted", added)
cv.waitKey(0)

