import numpy as np
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(image, [11,11], 0)
cv.imshow("Image", image)

edged = cv.Canny(blurred, 30, 150)
cv.imshow("Edges", edged)

[cnts, _] = cv.findContours(
	edged.copy(),
	cv.RETR_EXTERNAL,
	cv.CHAIN_APPROX_SIMPLE
)

print("I count {} coins in this image".format(len(cnts)))

coins = image.copy()
# -1 to draw all contours
cv.drawContours(coins, cnts, -1, [0, 255, 0], 2)

cv.imshow("Coins", coins)

for (i, c) in enumerate(cnts):
	(x, y, w, h) = cv.boundingRect(c)

	# make it not an index so that mere non-programmers can understand the
	# starting number of 1
	print("Coin #{}".format(i + 1))
	# a box around the coin based on its corner position, extended to the
	# right height and width
	coin = image[y:y+h, x:x+w]
	cv.imshow("Coin", coin)

	# create a mask to only show each coin; the mask will be the same dim
	# as the coin so it's cropped the same
	mask = np.zeros(image.shape[:2], dtype="uint8")
	[[centerX, centerY], radius] = cv.minEnclosingCircle(c)
	# indiv. coin mask
	cv.circle(mask, [int(centerX), int(centerY)], int(radius), 255, -1)
	mask = mask[y:y+h, x:x+w]
	cv.imshow("Masked Coin", cv.bitwise_and(coin, coin, mask=mask))

	cv.waitKey(0)