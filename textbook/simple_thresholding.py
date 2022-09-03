import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])

image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(image, [5,5], 0)
cv.imshow("Image", image)

# "rounds" or forces a pixel to a certain value; above thresh is white and
# below is black
[T, thresh] = cv.threshold(blurred, 155, 255, cv.THRESH_BINARY)
cv.imshow("Threshold Binary", thresh)

[T, threshInv] = cv.threshold(blurred, 155, 255, cv.THRESH_BINARY_INV)
cv.imshow("Threshold Binary Inverse", threshInv)

# apply the inverse threshold as a mask; this picks out the darker parts
# from the orig image since they will have been more black
cv.imshow("Text/Darker Parts", cv.bitwise_and(image, image, mask=threshInv))

cv.waitKey(0)