import numpy as np
import cv2 as cv

rectangleCanvas = np.ones([300, 300], dtype="uint8")
cv.rectangle(rectangleCanvas, [25, 25], [275, 275], 255, -1) # filled white rect
cv.imshow("Rectangle", rectangleCanvas)
cv.waitKey(0)

circleCanvas = np.zeros([300,300], dtype="uint8")
cv.circle(circleCanvas, [150, 150], 150, 255, -1) # filled white rect
cv.imshow("Circle", circleCanvas)
cv.waitKey(0)

bitwiseAnd = cv.bitwise_and(rectangleCanvas, circleCanvas)
cv.imshow("AND", bitwiseAnd)
cv.waitKey(0)

bitwiseOr = cv.bitwise_or(rectangleCanvas, circleCanvas)
cv.imshow("OR", bitwiseOr)
cv.waitKey(0)

bitwiseXor = cv.bitwise_xor(rectangleCanvas, circleCanvas)
cv.imshow("XOR", bitwiseXor)
cv.waitKey(0)

bitwiseNot = cv.bitwise_not(circleCanvas) # only circle here to flip its bits
cv.imshow("NOT", bitwiseNot)
cv.waitKey(0)