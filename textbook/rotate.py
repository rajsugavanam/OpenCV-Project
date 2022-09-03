import numpy as np
import argparse
import imutils
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

(x, y) = image.shape[:2] # exlude color
center = (x//2, y//2)

rotated = imutils.rotate(image, -45)
cv.imshow("Rotated by 45deg", rotated)
cv.waitKey(0)

rotated = imutils.rotate(image, -90)
cv.imshow("Rotated by -90deg", rotated)
cv.waitKey(0)
