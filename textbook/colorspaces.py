import argparse
import numpy as np
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("Gray", gray)

hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
cv.imshow("HSV", hsv)

lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
cv.imshow("L*a*b*", lab)
cv.waitKey(0)