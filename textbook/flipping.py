import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

flipped = cv.flip(image, 1) # across y axis flip
cv.imshow("Flipped Horizontally", flipped)
cv.waitKey(0)

flipped = cv.flip(image, 0)
cv.imshow("Flipped Vertically", flipped)
cv.waitKey(0)

flipped = cv.flip(image, -1)
cv.imshow("Flipped Horizontally & Vertically", flipped)
cv.waitKey(0)