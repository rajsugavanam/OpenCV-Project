import sys
sys.path.append("../../")

import cv2 as cv
import numpy as np
import sympy as sp

from opencv_project.math.ParsingTypes import ParsingTypes
from opencv_project.math.Equation import Equation
from opencv_project.math.DataPoint import DataPoint
from opencv_project.math.DataPointGenerator import DataPointGenerator

import argparse
import matplotlib


class GraphIllustrator(object):

	DEFAULT_CANVAS_SIZE_X:int = 500
	DEFAULT_CANVAS_SIZE_Y:int = 500
	DEFAULT_THICKNESS:int = 2
	DEFAULT_COLOR:tuple = (0,255,0)

	def __init__(self, canvas_size_x:int, canvas_size_y:int, dpg:DataPointGenerator, color:tuple[float, float, float], thickness:int) -> None:

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

	def plotDataPoints(self) -> None:
		"""
		Draws an illustration of the given data point list.
		"""
		print("Plotting graph points...")
		dpl = self.__dpg.getDataPoints()

		num_data_points = dpl.size()

		if (dpl.size() > 0):
			dpl.forEach(
				lambda dp: self.__drawDp(dp)
			)
		else:
			print("Failed to draw graph: No data points were found.")
		print("Done!")

	def showGraph(self):
		"""
		Open a window on your computer showing the canvas. Press any key to close it.
		"""
		cv.imshow("Graph", self.current_canvas)
		cv.waitKey(0)

	# color is in BGR
	def __drawDp(self, dp:DataPoint) -> None:
		"""
		Graphically draws a single line if the function is continuous,
		representing the connection between the last two iterated points.
		"""
		(center_x, center_y) = self.__getPixOrigin()
		(pix_x, pix_y) = self.__dpToPixel(dp)

		# only draw a connecting line if the function is continuous over the interval
		if self.__last_dp == None:
			self.__last_dp = dp
			return

		if ((self.__dpg.isDiscontinuous(self.__last_dp.getX(), dp.getX()) == False)):
			self.__last_dp = dp # cycle the datapoint
			# force the pixels within the valid integer range
			pix_x= max(-2**20, min(pix_x+center_x, 2**20)) # force the numbers to be a reasonable int without overflow
			pix_y= max(-2**20, min(center_y-pix_y, 2**20)) # we do minus because y starts from the top

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

	def __xPixInDrawRange(self, pix:int) -> None:
		"""
		Determine whether a given pixel `x` is in the current canvas.
		"""
		return (pix > 0 and pix < self.__len_x)

	def __yPixInDrawRange(self, pix:int) -> None:
		"""
		Determine whether a given pixel `y` is in the current canvas.
		"""
		return (pix > 0 and pix < self.__len_y)

	def __getPixOrigin(self) -> tuple[int, int]:
		"""
		Get the pixel coordinates corresponding to the center of the graph.
		"""
		(center_x, center_y) = (self.__len_x//2, self.__len_y//2)
		# get the x and y offset from the (x,y) point at the center of the screen,
		# and convert it to pixels. this is be the relative offset pixel offset to shift the
		# origin by.
		(offset_x, offset_y) = self.__dpToPixel(DataPoint(self.__dpg.getZeroXOffset(), self.__dpg.getZeroYOffset()))
		offset_x = offset_x+center_x
		offset_y = offset_y+center_y

		return (offset_x, offset_y)

	def __lerp(self) -> None:
		"""
		Linear Interpolate (draw a line) between the last two graphed points.
		This prevents gaps from a function changing in y value too much and allows
		`dx` to be smaller.
		"""
		if ((self.__linepos1 != None) and (self.__linepos2 != None)):
			cv.line(self.current_canvas, self.__linepos1, self.__linepos2, self.__graph_color, self.__graph_thickness)

	def __setPixel(self, x:int, y:int) -> None:
		"""
		Draw a circle at the given `x` and `y` pixel position.
		"""
		cv.circle(self.current_canvas, [x,y], thickness, color, -1)

	#TODO FIX
	def drawAxes(self, thickness:float=DEFAULT_THICKNESS, color:tuple[float, float, float]=(255,255,255)) -> None:
		(center_x, center_y) = self.__getPixOrigin()

		cv.line(self.current_canvas, (0, center_y), (self.__len_x, center_y), color, thickness)
		cv.line(self.current_canvas, (center_x, 0), (center_x, self.__len_y), color, thickness)

	def applySmoothing(self) -> None:
		self.current_canvas = cv.blur(self.current_canvas, [2,2])

	def __dpToPixel(self, dp:DataPoint) -> tuple[float,float]:
		"""
		Converts a `DataPoint` to a pixel coordinate.
		"""
		return (
			int(self.__pix_per_x*dp.getX()), int(self.__pix_per_y*dp.getY())
		)

	def __fixCanvasSizes(self, size_x:int, size_y:int, default_x:int=DEFAULT_CANVAS_SIZE_X, default_y:int=DEFAULT_CANVAS_SIZE_Y) -> None:
		"""
		Ensures that the canvas sizes were entered properly.
		"""
		if (size_x <= 0) or (size_y <= 0):
			print("Canvas dimensions cannot be equal to or less than zero. \
				Reverting to default.")
			self.current_canvas = np.zeros((default_y, default_x, 3), dtype="uint8")
		else:
			self.current_canvas = np.zeros((size_y, size_x, 3), dtype="uint8")

	# def __fixPixPerInt(self, pix_per_int:int, default:int=DEFAULT_PIX_PER_INT) -> None:
	# 	if pix_per_int <= 0:
	# 		print("Pixels per integer X cannot be less than or equal to 0. \
	# 			Reverting to default.")
	# 		self.pix_per_int:int = default
	# 	else:
	# 		self.pix_per_int:int = pix_per_int


def getArgumentColorOrDefault():
	if (args["color"] != None):
		rgb = matplotlib.colors.to_rgb(args["color"])
		return (rgb[2]*255, rgb[1]*255, rgb[0]*255)
	else:
		color = (0,255,0)

def getArgumentThicknessOrDefault():
	if (args["thickness"] != None):
		return args["thickness"]
	else:
		return 4


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("--color", "-c", required=False, help="A hex code representing the color of the graph.")
	ap.add_argument("--thickness", "-t", required=False, help="An integer representing the graph's line thickness.")
	# ap.add_argument("--xmin", required=True, help="The minimum x for the viewing plane.")
	# ap.add_argument("--xmax", required=True, help="The maximum x for the viewing plane.")
	# ap.add_argument("--ymin", required=True, help="The minimum y for the viewing plane.")
	# ap.add_argument("--ymax", required=True, help="The maximum y for the viewing plane.")
	args = vars(ap.parse_args())

	color = getArgumentColorOrDefault()
	thickness = getArgumentThicknessOrDefault()

	eq = Equation(parser_type=ParsingTypes.MATHEMATICA)
	# eq.askParser()
	eq.askEquation()
	# eq.askEquation()

	dpg = DataPointGenerator(eq, x_min=-10, x_max=10, y_min=-10, y_max=10, dx=0.025)
	# dpg = DataPointGenerator(eq, x_min=args["xmin"], x_max=args["xmax"], y_min=args["ymin"], y_max=args["ymax"], dx=0.1)
	dpg.generateDataPoints()

	illustrator = GraphIllustrator(2560, 1440, dpg, color, thickness)
	illustrator.drawAxes()
	illustrator.plotDataPoints()
	illustrator.applySmoothing()
	illustrator.showGraph()
