import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])

[B, G, R] = cv.split(image)

# they will be grayscale, 
# each pixel representing how much of each color is in each pixel
cv.imshow("Red", R)
cv.imshow("Green", G)
cv.imshow("Blue", B)
cv.waitKey(0)

merged = cv.merge([B, G, R])
cv.imshow("Merged", merged)
cv.waitKey(0)
cv.destroyAllWindows() # multiple windows were created