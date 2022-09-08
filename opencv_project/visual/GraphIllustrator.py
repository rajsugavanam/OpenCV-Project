import sys
sys.path.append("../../")

import cv2 as cv
import numpy as np

from opencv_project.math.ParsingTypes import ParsingTypes
from opencv_project.math.Equation import Equation
from opencv_project.math.DataPoint import DataPoint
from opencv_project.math.DataPointGenerator import DataPointGenerator


class GraphIllustrator(object):

	DEFAULT_CANVAS_SIZE_X:int = 500
	DEFAULT_CANVAS_SIZE_Y:int = 500
	DEFAULT_THICKNESS:float = 2
	DEFAULT_COLOR:tuple = (0,255,0)

	def __init__(self, canvas_size_x:int=DEFAULT_CANVAS_SIZE_X, canvas_size_y:int=DEFAULT_CANVAS_SIZE_Y) -> None:

		self.__fixCanvasSizes(canvas_size_x, canvas_size_y)
		
		self.len_x = self.current_canvas.shape[1]
		self.len_y = self.current_canvas.shape[0]
		self.pix_per_int = 1

	#TODO Function in need of redesign so that the function actually looks like a function!!!!!!!!
	def plotDataPoints(self, dpg:DataPointGenerator, thickness:float=DEFAULT_THICKNESS, color:tuple[float, float, float]=DEFAULT_COLOR) -> None:
		"""
		Draws an illustration of the given data point list.
		"""
		print("Plotting graph points...")
		dpl = dpg.getDataPoints()

		num_data_points = dpl.size()

		self.pix_per_int = int(self.len_x/dpg.getXRange())

		if (dpl.size() > 0):
			dpl.forEach(
				lambda dp: self.__drawDp(dp, thickness=thickness, color=color)
			)
		else:
			print("Failed to draw graph: No data points were found.")
		print("Done!")

	def showGraph(self):
		cv.imshow("Graph", self.current_canvas)
		cv.waitKey(0)

	# color is in BGR
	def __drawDp(self, dp, thickness:float=DEFAULT_THICKNESS, color:tuple[float, float, float]=DEFAULT_COLOR) -> None:
		"""
		Draws a single data point to the canvas.
		"""
		(center_x, center_y) = self.__getPixCenter()
		(pix_x, pix_y) = self.__dpToPixel(dp)

		pix_x=pix_x+center_x
		pix_y=center_y-pix_y # we do minus because y starts from the top

		# if the pixel coordinate is in the canvas
		if (pix_x > 0 and pix_x < self.len_x) and (pix_y > 0 and pix_y < self.len_y):
			self.__setPixel(pix_x, pix_y, thickness, color)

	def __getPixCenter(self) -> tuple[int, int]:
		(center_x, center_y) = (self.len_x//2, self.len_y//2)
		return (center_x, center_y)

	def __setPixel(self, x:int, y:int, thickness:float=DEFAULT_THICKNESS, color:tuple[int, int, int]=DEFAULT_COLOR) -> None:
		cv.circle(self.current_canvas, [x,y], thickness, color, -1)

	def drawAxes(self, thickness:float=DEFAULT_THICKNESS, color:tuple[float, float, float]=(255,255,255)) -> None:
		(center_x, center_y) = self.__getPixCenter()
		cv.line(self.current_canvas, (0, center_y), (self.len_x, center_y), color, thickness)
		cv.line(self.current_canvas, (center_x, 0), (center_x, self.len_y), color, thickness)

	def applySmoothing(self):
		self.current_canvas = cv.blur(self.current_canvas, [2,2])

	def __dpToPixel(self, dp:DataPoint) -> tuple[float,float]:
		"""
		Converts a `DataPoint` to a pixel coordinate.
		"""
		return (
			int(self.pix_per_int*dp.getX()), int(self.pix_per_int*dp.getY())
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


if __name__ == "__main__":
	eq = Equation(parser_type=ParsingTypes.MATHEMATICA)
	# eq.askParser()
	eq.askEquation()
	# eq.askEquation()

	dpg = DataPointGenerator(eq, x_min=-10, x_max=10, dx=0.001)
	dpg.generateDataPoints()

	illustrator = GraphIllustrator(canvas_size_x=1000, canvas_size_y=800)
	illustrator.drawAxes()
	illustrator.plotDataPoints(dpg, color=(100,100,100))
	# illustrator.applySmoothing()
	illustrator.showGraph()
