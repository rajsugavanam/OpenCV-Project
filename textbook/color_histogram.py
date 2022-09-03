from matplotlib import pyplot as plt
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)

channels = cv.split(image)

colors = ["b", "g", "r"]
plt.figure()
plt.title("Flattened Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")

# tuple/dict of color image as key, b g or r as val
# to assign them to colors
for [channel, color] in zip(channels, colors):
	hist = cv.calcHist([channel], [0], None, [256], [0, 256])
	plt.plot(hist, color=color) # change graph color to chan color and plot
	plt.xlim([0,256])

plt.show()
cv.waitKey(0)

fig = plt.figure()

ax = fig.add_subplot(131)
hist = cv.calcHist(
	[channels[1], channels[0]], 
	[0,1], 
	None, 
	[32,32], 
	[0, 256, 0, 256]
)
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for G and B")
plt.colorbar(p)

ax = fig.add_subplot(132)
hist = cv.calcHist(
	[channels[1], channels[2]], 
	[0,1], 
	None, 
	[32,32], 
	[0, 256, 0, 256]
)
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for G and R")
plt.colorbar(p)
ax = fig.add_subplot(132)
hist = cv.calcHist(
	[channels[1], channels[2]], 
	[0,1], 
	None, 
	[32,32], 
	[0, 256, 0, 256]
)
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for G and R")
plt.colorbar(p)
ax = fig.add_subplot(132)
hist = cv.calcHist(
	[channels[1], channels[2]], 
	[0,1], 
	None, 
	[32,32], 
	[0, 256, 0, 256]
)
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for G and R")
plt.colorbar(p)

ax = fig.add_subplot(133)
hist = cv.calcHist(
	[channels[0], channels[2]], 
	[0,1], 
	None, 
	[32,32], 
	[0, 256, 0, 256]
)
p = ax.imshow(hist, interpolation="nearest")
ax.set_title("2D Color Histogram for B and R")
plt.colorbar(p)

print("2D histogram shape: {}, with {} values"
	.format(hist.shape, hist.flatten().shape[0])
)