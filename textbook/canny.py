import numpy as np
import argparse
import cv2 as cv
import mahotas

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
image = cv.GaussianBlur(image, [5,5], 0)
cv.imshow("Blurred", image)

# for pixel intensities:
# above 150 is an edge
# below 30 is not an edge
# between 30 and 150 depends on how intensities are connected
canny = cv.Canny(image, 30, 150)
cv.imshow("Canny", canny)
cv.waitKey(0)