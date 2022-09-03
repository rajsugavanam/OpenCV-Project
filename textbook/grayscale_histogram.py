from matplotlib import pyplot as plt
import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])

image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("Original", image)

hist = cv.calcHist([image], [0], None, [256], [0,256])

plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of pixels")
plt.plot(hist)
plt.xlim([0, 256])
plt.show()
cv.waitKey(0)

# frequencies of grayscale color values 0-255