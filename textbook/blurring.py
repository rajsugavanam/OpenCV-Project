import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])
# cv.imshow("Original", image)

blurred = np.hstack([
	cv.blur(image, [3,3]),
	cv.blur(image, [5,6]),
	cv.blur(image, [7,7])
])
cv.imshow("Averaged", blurred)

blurred = np.hstack([
	cv.medianBlur(image, 3),
	cv.medianBlur(image, 5),
	cv.medianBlur(image, 7)
])
cv.imshow("Median", blurred)

blurred = np.hstack([
	cv.bilateralFilter(image, 3, 21, 21),
	cv.bilateralFilter(image, 5, 31, 31),
	cv.bilateralFilter(image, 7, 41, 41)
])
cv.imshow("Bilateral", blurred)

cv.waitKey(0)