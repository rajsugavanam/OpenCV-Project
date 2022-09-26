import sys
sys.path.append("../../")

from graph_math.Equation import Equation

import cv2 as cv
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt

import array

class GraphImage(object):
	"""
	Has functionalities to manipulate final graph images.
	"""
# ---------------------------------------------------------------------------- #
	def __init__(self, graph_image:array) -> None:
		self.graph_image = graph_image
# ---------------------------------------------------------------------------- #
	def showGraphHist(self) -> None:
		"""
		Shows a histogram of the current graph image, which represents how much
		screenspace the drawn graph takes up.
		"""
		#! [TEXTBOOK] 3D Histogram
		hist = cv.calcHist(
			[self.graph_image], 
			[0, 1, 2], 
			None, 
			[256, 256, 256],
			[0, 256, 0, 256, 0, 256]
		)

		fig = plt.figure()
		subplot = fig.add_subplot(111, projection="3d")

		# go through every pixel
		print("Calculating Histogram...")
		self.__fillSubplotHist(hist, subplot)

		plt.title("Graph Histogram (Size = Frequency)")
		subplot.set_xlabel("B")
		subplot.set_ylabel("G")
		subplot.set_zlabel("R")
		print("Done!")
		plt.show()
# ---------------------------------------------------------------------------- #
	def __fillSubplotHist(self, hist, sub_plot) -> None:
		"""
		Go through every pixel color in a histogram and fill a 3D subplot with
		its color frequencies.
		"""
		# go through every pixel
		for (x, plane) in enumerate(hist):
			for (y, row) in enumerate(plane):
				for (z, col) in enumerate(row):
					# color amount
					__coloramt = hist[x][y][z]
					# don't plot black
					if __coloramt > 0.0 \
						and (x,y,z) != (0,0,0):

						# convert (255,255,255) to (1.0, 1.0, 1.0)
						__face_colors = \
							(z / 255,
							y / 255,
							x / 255)

						# plot the color as vector/point with dot size as
						# frequency
						sub_plot.scatter(
							x, y, z,
							s=0.05*__coloramt, 
							facecolors = __face_colors
						)
# ---------------------------------------------------------------------------- #
	def showGraph(self) -> None:
		"""
		Open a window on your computer showing the processed image.
		`cv.waitKey()` may need to be used.
		"""
		cv.imshow("Graph", self.graph_image)
# ---------------------------------------------------------------------------- #
	def saveGraph(self, file_name) -> None:
		"""
		Saves the graph image under the given name
		to disk in a folder relative to this file.
		"""
		cv.imwrite(file_name, self.graph_image)
		print("Your graph has been saved as {}!"
			.format(file_name)
		)
# ---------------------------------------------------------------------------- #
	def applySmoothing(self, magnitude:int) -> None:
		"""
		Applies the standard OpenCV blur to the image.
		`magnitude`: The intensity of the blur to apply.
		"""
		#! [TEXTBOOK] Smoothing/Blurring
		self.graph_image = cv.blur(self.graph_image, [magnitude,magnitude])
# ---------------------------------------------------------------------------- #
	def showLatexFunction(self) -> None:
		"""
		Shows LaTeX text from an image on a graph. This should be the entered
		equation.
		"""
		#! Overlaying Images
		#! [TEXTBOOK] Resizing, Thresholding
		graph_x = self.graph_image.shape[1]
		graph_y = self.graph_image.shape[0]

		latex_image = cv.imread("function.png")
		
		# invert image colors
		[_, latex_image] = \
			cv.threshold(latex_image, 155, 255, cv.THRESH_BINARY_INV)

		len_x = latex_image.shape[1]
		len_y = latex_image.shape[0]

		resize_factor = sp.sqrt(graph_x*graph_y)/2000
		latex_image = \
			cv.resize(
				latex_image, 
				(int(len_x*resize_factor),
				int(len_y*resize_factor)),
				interpolation=cv.INTER_AREA
			)

		len_x = latex_image.shape[1]
		len_y = latex_image.shape[0]
		OFFSET = 20

		self.graph_image \
			[OFFSET:len_y+OFFSET, OFFSET:len_x+OFFSET] = latex_image
# ---------------------------------------------------------------------------- #