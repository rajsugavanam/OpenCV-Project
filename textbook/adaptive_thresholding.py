import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])

image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(image, [5,5], 0)
cv.imshow("Image", image)

thresh = cv.adaptiveThreshold(
	blurred,
	255,
	cv.ADAPTIVE_THRESH_MEAN_C,
	cv.THRESH_BINARY_INV,
	11,
	4
)
cv.imshow("Mean Thresh", thresh)

thresh = cv.adaptiveThreshold(
	blurred,
	255,
	cv.ADAPTIVE_THRESH_GAUSSIAN_C,
	cv.THRESH_BINARY_INV,
	15,
	3
)
cv.imshow("Gaussian Thresh", thresh)

cv.waitKey(0)