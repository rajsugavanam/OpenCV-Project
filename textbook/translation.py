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

# i-hat+25 and j-hat+50
shifted = imutils.translate(image, 25, 50)
cv.imshow("Shifted Down and Right", shifted)
cv.waitKey(0)

shifted = imutils.translate(image, -50, -90)
cv.imshow("Shifted Down and Left", shifted)

cv.waitKey(0)

