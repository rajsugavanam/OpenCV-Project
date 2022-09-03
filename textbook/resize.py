import numpy as np
import argparse
import imutils
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

r = 150.0 / image.shape[1]
dim = (150, int(image.shape[0]*r)) # correspondingly scale y

# scale and keep ratio (diagonal scale)
# resized = imutils.resize(image, 150)
resized = cv.resize(image, dim, interpolation=cv.INTER_AREA)
cv.imshow("Resized (Width)", resized)
cv.waitKey(0)

