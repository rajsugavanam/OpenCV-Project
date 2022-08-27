import numpy as np
import cv2 as cv

canvas = np.zeros((300,300,3), dtype="uint8")

green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)

cv.line(canvas, (0,0),(300,300), green)
cv.line(canvas, (300,0), (0,300), red, 3)
cv.rectangle(canvas, (10,10), (60,60), green)
cv.rectangle(canvas, (50,200), (200,255), red, 5)
cv.rectangle(canvas, (200,50), (255,125), blue, -1)

cv.imshow("Canvas", canvas)
cv.waitKey()