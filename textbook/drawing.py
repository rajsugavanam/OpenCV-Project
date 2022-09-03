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
cv.waitKey(0)

#* CLEAR CANVAS
canvas = np.zeros((300,300,3), dtype="uint8")
(centerX, centerY) = (canvas.shape[1] // 2, canvas.shape[0] // 2)

for r in range(0,175,25): # 7 circle radii with 25 radii diff
	cv.circle(canvas, (centerX, centerY), r, (255,255,255))

cv.imshow("Canvas", canvas)
cv.waitKey(0)

# ------------------------------ Random Circles ------------------------------ #
for i in range(0,25): # repeat operation 25x
	radius = np.random.randint(5, 200)
	color = np.random.randint(0, 256, size=(3,) ).tolist()
	pt = np.random.randint(0, 300, size=(2,))
	cv.circle(canvas, tuple(pt), radius, color, -1) # -1 thick for solid

cv.imshow("Canvas", canvas)
cv.waitKey(0)