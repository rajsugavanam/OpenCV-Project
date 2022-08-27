import numpy as np
import cv2 as cv
import scipy as sp
import math

f = lambda x: math.sin(x)

xMax = 10
xMin = -10
deltaX=xMax-xMin

yMax = 10
yMin = -10
deltaY = yMax-yMin

resolution = 0.01

canvas = np.zeros((deltaX,deltaY,3), dtype="uint8")

for i in range(0, deltaX):
	x = i+xMin
	print(i)
	y = f(x)
	if y >= 0 or y <= deltaY:
		canvas[i, y] = (0,255,0)

cv.imshow("Graph", canvas)
cv.waitKey()