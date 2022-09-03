import numpy as np
import argparse
import cv2 as cv
import mahotas

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("Original", image)

lap = cv.Laplacian(image, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow("Laplacian", lap)
cv.waitKey(0)

sobelX = cv.Sobel(image, cv.CV_64F, 1, 0)
sobelY = cv.Sobel(image, cv.CV_64F, 0, 1)

sobelX = np.uint8(np.absolute(sobelX))
sobelY = np.uint8(np.absolute(sobelY))

sobelCombined = cv.bitwise_or(sobelX, sobelY)

cv.imshow("Sobel X", sobelX)
cv.imshow("Sobel Y", sobelY)
cv.imshow("Sobel Combined", sobelCombined)
cv.waitKey(0)