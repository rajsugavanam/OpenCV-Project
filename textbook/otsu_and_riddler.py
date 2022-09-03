import numpy as np
import argparse
import cv2 as cv
import mahotas

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])

image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(image, [5,5], 0)
cv.imshow("Image", image)

# OTSU
# ---------------------------------------------------------------------------- #
# compute thresh value
T = mahotas.thresholding.otsu(blurred)
print("Otsu's Threshold: {}".format(T))

thresh = image.copy()
thresh[thresh > T] = 255 # if above thresh, make 255
thresh[thresh < 255] = 0 # make any pixels that didnt go above thresh black
thresh = cv.bitwise_not(thresh)
cv.imshow("Otsu", thresh)
# ---------------------------------------------------------------------------- #

# RIDDLER
# ---------------------------------------------------------------------------- #
T = mahotas.thresholding.rc(blurred)
print("Riddler-Calvard: {}".format(T))

thresh = image.copy()
thresh[thresh > T] = 255
thresh[thresh < 255] = 0
thresh = cv.bitwise_not(thresh)
cv.imshow("Riddler-Calvard", thresh)
# ---------------------------------------------------------------------------- #
cv.waitKey(0)