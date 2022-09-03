import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)
cv.waitKey(0)

mask = np.zeros(image.shape[:2], dtype="uint8")
[centerX, centerY] = (image.shape[1] // 2, image.shape[0] // 2)
# add centered white square to previously blank mask
cv.rectangle(mask, (centerX - 75, centerY - 75), (centerX + 75, centerY + 75), 255, -1)
# cv.circle(mask, [centerX, centerY], 100, 255, -1)
cv.imshow("Mask", mask)
cv.waitKey(0)

# only applies the mask
masked = cv.bitwise_and(image, image, mask=mask)
cv.imshow("Mask applied to image", masked)
cv.waitKey(0)