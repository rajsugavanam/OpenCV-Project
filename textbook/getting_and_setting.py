import argparse
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow("Original", image)

(b,g,r) = image[0,0] # pix at (0,0)

print("Pixel at (0,0) - Red: {}, Green: {}, Blue: {}".format(r,g,b))

image[0,0] = (0,0,255) #set to red
print("Pixel at (0,0) - Red: {}, Green: {}, Blue: {}".format(r,g,b))

corner = image[0:100, 0:100] # corner square
cv.imshow("Corner", corner)

image[0:100, 0:100] = (0,255,0)

cv.imshow("Updated", image) # show updated image with green @ top left
cv.waitKey(0)