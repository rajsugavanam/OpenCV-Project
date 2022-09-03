from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2 as cv

def plot_histogram(image, title, mask = None):
	channels = cv.split(image)
	colors = ["b", "g", "r"]
	plt.figure()
	plt.title(title)
	plt.xlabel("Bins")
	plt.ylabel("# of Pixels")

	for [channel, color] in zip(channels, colors):
		hist = cv.calcHist([channel], [0], mask, [256], [0,256])
		plt.plot(hist, color=color)
		plt.xlim([0,256])

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)

mask = np.zeros(image.shape[:2], dtype="uint8")
cv.rectangle(mask, [15,15], [130,100], 255, -1)
cv.imshow("Mask", mask)

# only apply the mask
masked = cv.bitwise_and(image, image, mask=mask)
cv.imshow("Applying the mask", masked)

plot_histogram(image, "Histogram for Original Image", mask=mask)

plt.show()