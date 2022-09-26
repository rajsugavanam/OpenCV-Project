from os import system

import sys
sys.path.append("../../")

import cv2 as cv
import numpy as np
import sympy as sp

from graph_math.ParsingTypes import ParsingTypes
from graph_math.Equation import Equation
from graph_math.DataPoint import DataPoint
from graph_math.DataPointGenerator import DataPointGenerator
from visual.GraphImage import GraphImage

import argparse
from tqdm import tqdm
from array import array

import matplotlib
from matplotlib import pyplot as plt


class GraphIllustrator(object):
	"""
	Uses the data from a `DataPointGenerator` to visually draw out its function.
	"""

	__DEFAULT_CANVAS_SIZE_X:int = 500
	__DEFAULT_CANVAS_SIZE_Y:int = 500
	__DEFAULT_THICKNESS:int = 2
	__DEFAULT_COLOR:tuple = (0,255,0)
# ---------------------------------------------------------------------------- #
	def __init__(self, canvas_size_x:int, canvas_size_y:int, dpg:DataPointGenerator, 
		color:tuple[float, float, float], thickness:int) -> None:

		self.__fixCanvasSizes(canvas_size_x, canvas_size_y)
		
		self.__len_x:int = self.current_canvas.shape[1]
		self.__len_y:int = self.current_canvas.shape[0]

		self.__graph_color:tuple[float, float, float] = color
		self.__graph_thickness:int = int(thickness)

		self.__linepos1:tuple[int, int] = None
		self.__linepos2:tuple[int, int] = None

		self.__last_dp:DataPoint = None

		self.__dpg:DataPointGenerator = dpg

		self.__pix_per_x:int = int(self.__len_x/self.__dpg.getXRange())
		self.__pix_per_y:int = int(self.__len_y/self.__dpg.getYRange())
# ---------------------------------------------------------------------------- #
	def maskedWithEquation(self, equation:Equation) -> array:
		"""
		Masks/intersects this graph's equation with another equation, returning
		it as a new image.
		"""
		#! [TEXTBOOK] Masking
		eq_masker = self.__equationMasker(equation)

		print("Preparing mask equation...")
		eq_masker.__getDataPointGenerator().generateDataPoints()
		eq_masker.drawGraph()

		# masks can only be 1 channel, so make the mask image grayscale
		grayscale_mask = \
			cv.cvtColor(eq_masker.getGraphImage(), cv.COLOR_BGR2GRAY)

		# mask the current graph with the new mask graph
		masked = cv.bitwise_and(
			self.current_canvas,
			self.current_canvas,
			mask=grayscale_mask
		)

		return masked
# ---------------------------------------------------------------------------- #
	def __equationMasker(self, equation:Equation) -> "GraphIllustrator":
		"""
		Clones this `GraphIllustrator` instance with a different equation,
		primed with a white color. Its graph image can serve as a mask.
		"""
		new_dpg = self.__getDataPointGenerator().cloneToNewDpg(equation)
		gi = GraphIllustrator(
			self.getSizeX(),
			self.getSizeY(),
			new_dpg,
			(255,255,255),
			self.getThickness()
		)

		return gi
# ---------------------------------------------------------------------------- #
	def __getDataPointGenerator(self) -> DataPointGenerator:
		"""
		Gets the `DataPointGenerator` stored in this illustrator.
		"""
		return self.__dpg
# ---------------------------------------------------------------------------- #
	def getGraphImage(self) -> array:
		"""
		Gets the canvas object of the graph.
		"""
		return self.current_canvas
# ---------------------------------------------------------------------------- #
	def getSizeX(self) -> float:
		"""
		Gets the pixel width of the graph image.
		"""
		return self.__len_x
# ---------------------------------------------------------------------------- #
	def getSizeY(self) -> float:
		"""
		Gets the pixel height of the graph image.
		"""
		return self.__len_y
# ---------------------------------------------------------------------------- #
	def getColor(self) -> float:
		"""
		Gets the color of the function curve.
		"""
		return self.__graph_color
# ---------------------------------------------------------------------------- #
	def setColor(self, color:tuple[float,float,float]) -> float:
		"""
		Sets the color of the function curve.
		"""
		self.__graph_color = color
# ---------------------------------------------------------------------------- #
	def getThickness(self) -> float:
		"""
		Gets the thickness of the function curve.
		"""
		return self.__graph_thickness
# ---------------------------------------------------------------------------- #
	def setThickness(self, thickness:float) -> float:
		"""
		Sets the thickness of the function curve.
		"""
		self.__graph_thickness = thickness
# ---------------------------------------------------------------------------- #
	def drawGraph(self) -> None:
		"""
		Draws an illustration of the given data point list.
		"""
		print("Drawing graph...")
		dpl = self.__dpg.getDataPoints()

		num_data_points = dpl.size()

		if (dpl.size() > 0):
			dpl.forEach(
				lambda dp: self.__drawDp(dp)
			)
		else:
			print("Failed to draw graph: No data points were found.")
		print("Done!")
# ---------------------------------------------------------------------------- #
	def showGraph(self) -> None:
		"""
		Open a window on your computer showing the canvas. Press any key to close it.
		"""
		cv.imshow("Graph", self.current_canvas)
		cv.waitKey(0)
# ---------------------------------------------------------------------------- #
	def setDataPointGenerator(self, dpg:DataPointGenerator) -> None:
		"""
		Replaces the illustrator's `DataPointGenerator`.
		"""
		self.__dpg = dpg
# ---------------------------------------------------------------------------- #
	# color is in BGR
	def __drawDp(self, dp:DataPoint) -> None:
		"""
		Graphically draws a single line if the function is continuous,
		representing the connection between the last two iterated points.\n
		`dp`: The `DataPoint` to draw a line from the previous `DataPoint` to.
		"""
		(center_x, center_y) = self.__getPixOrigin()
		(pix_x, pix_y) = self.__dpToPixel(dp)

		# only draw a connecting line if the function is continuous over the interval
		if self.__last_dp == None:
			self.__last_dp = dp
			return

		if (self.__dpg.checkDerivative(self.__last_dp, dp)):

			self.__last_dp = dp # cycle the datapoint
			# force the pixels within the valid integer range
			pix_x = max(-2**20, min(pix_x+center_x, 2**20)) # force the numbers to be a reasonable int without overflow
			pix_y = max(-2**20, min(center_y-pix_y, 2**20)) # we do minus because y starts from the top

			# transition points to describe a line between the next two points
			self.__linepos1 = self.__linepos2
			self.__linepos2 = (pix_x, pix_y)

			# if the pixel x coordinate is in the canvas.
			# we don't check for y being in the canvas because sometimes the point
			# we need to lerp to is in the x-range, but not the y-range.
			if self.__xPixInDrawRange(pix_x):
				# at this point both this and the previous pixel are in the canvas,
				# so we can lerp
				self.__lerp()
			# self.__setPixel(pix_x, pix_y, thickness, color)
		else:
			self.__last_dp = None
			self.__linepos1 = None
			self.__linepos2 = None
# ---------------------------------------------------------------------------- #
	def __xPixInDrawRange(self, pix:int) -> None:
		"""
		Determine whether a given pixel `x` is in the current canvas.
		"""
		return (pix > 0 and pix < self.__len_x)
# ---------------------------------------------------------------------------- #
	def __yPixInDrawRange(self, pix:int) -> None:
		"""
		Determine whether a given pixel `y` is in the current canvas.
		"""
		return (pix > 0 and pix < self.__len_y)
# ---------------------------------------------------------------------------- #
	def __getPixOrigin(self) -> tuple[int, int]:
		"""
		Get the pixel coordinates corresponding to the center of the graph.
		"""
		(center_x, center_y) = (self.__len_x//2, self.__len_y//2)
		# get the x and y offset from the (x,y) point at the center of the screen,
		# and convert it to pixels. this is be the relative offset pixel offset to shift the
		# origin by.
		(offset_x, offset_y) = self.__dpToPixel(
			DataPoint(self.__dpg.getZeroXOffset(), self.__dpg.getZeroYOffset())
		)
		offset_x = offset_x+center_x
		offset_y = offset_y+center_y

		return (offset_x, offset_y)
# ---------------------------------------------------------------------------- #
	def __lerp(self) -> None:
		"""
		Linear Interpolate (draw a line) between the last two graphed points.
		This prevents gaps from a function changing in y value too much and
		gives room for the points' `Δx` to be larger.
		"""
		#! [TEXTBOOK] Drawing (lines)
		if ((self.__linepos1 != None) and (self.__linepos2 != None)):
			cv.line(
				self.current_canvas, self.__linepos1, self.__linepos2, 
				self.__graph_color, self.__graph_thickness
			)
# ---------------------------------------------------------------------------- #
	def __setPixel(self, x:int, y:int) -> None:
		"""
		Draw a circle at the given `x` and `y` pixel position.
		"""
		cv.circle(self.current_canvas, [x,y], thickness, color, -1)
# ---------------------------------------------------------------------------- #
	def drawAxes(self, thickness:float=__DEFAULT_THICKNESS, 
		color:tuple[float, float, float]=(255,255,255)) -> None:
		"""
		Draws out `x` and `y` axes based on what the bounds are set to.
		`thickness`: The thickness of the axis lines.
		`color`: The color of the axis lines.
		"""

		(center_x, center_y) = self.__getPixOrigin()

		# draw x axis
		cv.line(self.current_canvas, (0, center_y), (self.__len_x, center_y), 
			color, thickness)
		# draw y axis
		cv.line(self.current_canvas, (center_x, 0), (center_x, self.__len_y), 
			color, thickness)

		# save the ranges so they don't have to be recalculated
		__x_range = self.__dpg.getXRange()
		__y_range = self.__dpg.getYRange()
		
		# the portion of the screen that has a tick. if x goes from
		# -2 to 2, the range is 4 and the x multiplier will be 2/4 = 1/2
		# of the screen. (the tick will span -1 to 1).
		__tick_len_mult = 1/__x_range
		__tick_height_mult = 1/__y_range

		# easy constant to scale the height
		TICK_SPAN = 20

		# actual tick height and length in pixels
		__tick_len = int(self.__len_x*__tick_len_mult)
		__tick_height = int(self.__len_y*__tick_height_mult)

		# draw x ticks
		# ceiling is used because if you have 0.5 as the max, the closest
		# max integer that includes it is its ceiling
		for x_i in np.arange(self.__getViewingOffsetX(), sp.ceiling(__x_range)):
			__horizontal_position = int(x_i*__tick_len)
			cv.line(
				self.current_canvas,
				(__horizontal_position, center_y-TICK_SPAN),
				(__horizontal_position, center_y+TICK_SPAN),
				color, thickness)

		# draw y ticks
		for y_i in np.arange(self.__getViewingOffsetY(), sp.ceiling(__y_range)):
			__vert_position = int(y_i*__tick_height)
			cv.line(
				self.current_canvas,
				(center_x-TICK_SPAN, __vert_position),
				(center_x+TICK_SPAN, __vert_position),
				color, thickness)

# ---------------------------------------------------------------------------- #
	def __getViewingOffsetX(self) -> float:
		"""
		Gets the difference between the minimum `x` value and its floor.
		This is essentially how far the viewing plane is shifted to the right
		from the left-most closest integer.
		"""
		__min_x = self.__dpg.getMinX()
		__x_before_least = sp.floor(__min_x)
		__x_min_difference = __min_x-__x_before_least
		return __x_min_difference
# ---------------------------------------------------------------------------- #
	def __getViewingOffsetY(self) -> float:
		"""
		Gets the difference between the maximum `y` value and its floor.
		This is essentially how far the viewing plane is shifted downwards
		from the top-most closest integer.
		"""
		__max_y = self.__dpg.getMaxY()
		__y_after_most = sp.ceiling(__max_y)
		__y_min_difference = __y_after_most-__max_y
		return __y_min_difference
# ---------------------------------------------------------------------------- #
	"""
	Unused due to problems with the axes counting as contours!
	"""
	# def cropToFunction(self):
	# 	"""
	# 	Uses contour detection to crop the graph image to bound only the
	# 	function.
	# 	"""
	# 	# grayscale
	# 	__grayscale_graph = cv.cvtColor(self.current_canvas, cv.COLOR_BGR2GRAY)
	# 	# remove axes
	# 	[T, __grayscale_graph] = \
	# 		cv.threshold(__grayscale_graph, 255, 255, cv.THRESH_BINARY)

	# 	cv.imshow("Gray", __grayscale_graph)

	# 	# grab contours
	# 	[contours, _] = cv.findContours(
	# 		__grayscale_graph,
	# 		cv.RETR_EXTERNAL,
	# 		cv.CHAIN_APPROX_SIMPLE
	# 	)

	# 	# initial min and max contour values: make them the lowest respectively
	# 	__min_x = self.__len_x
	# 	__min_y = self.__len_y # these are usually maximum values;
	# 						   # these will be quickly reduced from the
	# 						   # contours' mins
	# 	__max_x = 0
	# 	__max_y = 0 # opposite procedure from above

	# 	# collect/update max and min values for contours
	# 	cv.drawContours(self.current_canvas, contours, -1, [0, 255, 0], 2)
	# 	cv.imshow("conts", self.current_canvas)
	# 	cv.waitKey(0)

	# 	for (i, contour) in enumerate(contours):
	# 		(__x, __y, __w, __h) = cv.boundingRect(contour)
	# 		__min_x = min(__x, __min_x)
	# 		__min_y = min(__y, __min_y)
	# 		__max_x = max(__x+__w, __max_x)
	# 		__max_y = max(__y+__h, __max_y)

	# 	# crop to bounding region
	# 	self.current_canvas = self.current_canvas[
	# 		__min_x:__max_x,
	# 		__min_y:__max_y
	# 	]
# ---------------------------------------------------------------------------- #
	def __dpToPixel(self, dp:DataPoint) -> tuple[float,float]:
		"""
		Converts a `DataPoint` to a pixel coordinate.
		Returns: A pixel coordinate in the form `(x,y)`.
		"""
		return (
			int(self.__pix_per_x*dp.getX()), int(self.__pix_per_y*dp.getY())
		)
# ---------------------------------------------------------------------------- #
	def __fixCanvasSizes(self, size_x:int, size_y:int, 
		default_x:int=__DEFAULT_CANVAS_SIZE_X, 
		default_y:int=__DEFAULT_CANVAS_SIZE_Y) -> None:
		"""
		`INTERNAL FUNCTION:` Ensures that the canvas sizes were entered properly.\n
		Do not use!
		"""
		if (size_x <= 0) or (size_y <= 0):
			print("Canvas dimensions cannot be equal to or less than zero. \
				Reverting to default.")
			self.current_canvas = np.zeros((default_y, default_x, 3), dtype="uint8")
		else:
			self.current_canvas = np.zeros((size_y, size_x, 3), dtype="uint8")
# ---------------------------------------------------------------------------- #
	def clearCanvas(self) -> None:
		"""
		Clears the canvas.
		"""
		self.current_canvas = \
		np.zeros(
			(self.__len_y, self.__len_x, 3), 
			dtype="uint8"
		)
# ---------------------------------------------------------------------------- #
	# def __fixPixPerInt(self, pix_per_int:int, default:int=DEFAULT_PIX_PER_INT) -> None:
	# 	if pix_per_int <= 0:
	# 		print("Pixels per integer X cannot be less than or equal to 0. \
	# 			Reverting to default.")
	# 		self.pix_per_int:int = default
	# 	else:
	# 		self.pix_per_int:int = pix_per_int


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("--color", "-c", required=False, 
		help="A hex code representing the color of the graph.")
	ap.add_argument("--thickness", "-t", required=False, 
		help="An integer representing the graph's line thickness.")
	# ap.add_argument("--xmin", required=True, help="The minimum x for the viewing plane.")
	# ap.add_argument("--xmax", required=True, help="The maximum x for the viewing plane.")
	# ap.add_argument("--ymin", required=True, help="The minimum y for the viewing plane.")
	# ap.add_argument("--ymax", required=True, help="The maximum y for the viewing plane.")
	args = vars(ap.parse_args())

	color = getArgumentColorOrDefault()
	thickness = getArgumentThicknessOrDefault()

# --------------------------- Construct Main Graph --------------------------- #
	eq = Equation(parser_type=ParsingTypes.LATEX)
	# eq.askParser()
	print("-------------------------------------------------------")

	print("\033[92;1mMain equation:\033[0m")
	eq.askEquation()
	print("-------------------------------------------------------")
	dpg = DataPointGenerator(eq, x_min=-10, x_max=10, y_min=-5, y_max=5)
	dpg.generateDataPoints()
	print("-------------------------------------------------------")
	illustrator = GraphIllustrator(2560, 1440, dpg, color, thickness)
	illustrator.drawAxes()
	illustrator.drawGraph()
	print("-------------------------------------------------------")
	
# ------------------- Mask the main graph from an equation ------------------- #
	# MASKING TEST
	eq2 = Equation(parser_type=ParsingTypes.LATEX)
	print("-------------------------------------------------------")
	print("\033[1mMask equation:\033[0m")
	eq2.askEquation()
	print("-------------------------------------------------------")
	masked = illustrator.maskedWithEquation(eq2)
	
	cv.imshow("Masked", masked)
	cv.waitKey(0)
# ------------------------- Smoothing, Histogram, Etc ------------------------ #
	# Graph image manipulation
	gimg = GraphImage(illustrator.getGraphImage())
	gimg.applySmoothing(3)
	gimg.showGraph()
	# gimg.showGraphHist()
	# print("-------------------------------------------------------")

	cv.waitKey(0)
	system("cls||clear")
# -------------------------------- Save Image -------------------------------- #
	gimg.saveGraph("saved_graph.jpg")
