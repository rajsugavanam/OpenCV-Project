import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

cropped = image[30:120, 240:335]
cv.imshow("Cropped Image", cropped)
cv.waitKey(0)