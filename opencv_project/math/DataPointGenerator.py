import sys

sys.path.append("../../")

import numpy as np
from tqdm import tqdm

from opencv_project.math.Equation import Equation
from opencv_project.math.DataPoint import DataPoint
from opencv_project.math.DataPointList import DataPointList

class DataPointGenerator(object):

	def __init__(self, equation:Equation, x_min:float=-10, x_max:float=10, y_min:float=-10, y_max:float=10, dx:float=0.001) -> None:
		self.__equation:Equation = equation
		self.__data_points:DataPointList = DataPointList()

		self.__fixEnteredBounds(x_min, x_max, y_min, y_max)

		if dx <= 0:
			print("The dx value must not be lower than or equal to 0. Reverting to default value.")
			self.__dx = 0.001
		else:
			self.__dx = dx

	def getEquation(self) -> None:
		"""
		(`Equation`) Returns the stored equation.
		"""
		return self.__equation

	def getStoredFunction(self):
		"""
		(`function`) Returns the stored function `f(x)`.
		"""
		return self.__equation.getStoredFunction()

	def setDx(self, dx:float) -> None:
		"""
		Set the value for `dx`. this is the delta between x values\n
		(or the spacing) between the `x` data points.
		"""
		self.__dx = dx

	def getDx(self):
		"""
		Get the value for `dx`. this is the delta between x values\n
		(or the spacing) between the `x` data points.
		"""
		return self.__dx

	def getDataPoints(self) -> DataPointList:
		"""
		Get the list of data points calculated for the function `f(x)`.\n
		"""
		return self.__data_points

	def __addDataPoint(self, data_point:DataPoint) -> None:
		"""
		Add a `DataPoint` to the generator's list.
		"""
		self.__data_points.addOrChangeDataPoint(data_point)

	def getXRange(self) -> float:
		return self.__gen_max_x - self.__gen_min_x

	def setGenerationBoundX(self, min_x:float, max_x:float, generate:bool=True) -> None:
		"""
		Set the `x` bound to generate values in.\n
		`min_x`: the minimum `x` value to generate points in.\n
		`max_x`: the maximum `x` value to generate points in.\n
		`generate`: whether to generate additional points if the bound was expanded.
		"""
		if (self.__boundValid(min_x, max_x)):
			expanded:bool = self.__boundExpanded(min_x, self.__gen_min_x, self.__gen_max_x, max_x)

			self.__gen_min_x = min_x
			self.__gen_max_x = max_x

			if generate and expanded:
				self.generateDataPoints()
		else:
			print("The lower X bound must be higher than the higher X bound.\nBound was not set.")

	def setGenerationBoundY(self, min_y:float, max_y:float, generate:bool=True) -> None:
		"""
		Set the `y` bound to generate values in.\n
		`min_y`: the minumum `y` value to generate points in.\n
		`max_y`: the maximum `y` value to generate points in.\n
		`generate`: whether to generate additional points if the bound was expanded.
		"""
		if (self.__boundValid(min_y, max_y)):
			expanded:bool = self.__boundExpanded(min_y, self.__gen_min_y, self.__gen_max_y, max_y)

			self.__gen_min_y = min_y
			self.__gen_max_y = max_y

			if generate and expanded:
				self.generateDataPoints()
		else:
			print("The lower Y bound must be higher than the higher Y bound.\nBound was not set.")

	def __boundExpanded(self, low:float, current_low:float, current_high:float, high:float) -> bool:
		return (low < current_low) or (current_high > high)

	def __boundValid(self, min_val:float, max_val:float):
		return (min_val<max_val)

	def __fixEnteredBounds(self, x_min:float, x_max:float, y_min:float, y_max:float) -> None:
		"""
		Verify the bounds entered for this class. If any are invalid, the bounds
		will revert to their defaults.
		"""
		if (self.__boundValid(x_min, x_max) and self.__boundValid(y_min, y_max)) == False:
			print("The lower bounds must be higher than the higher bounds. Reverting to default value.")
			self.__gen_min_x:float = -10
			self.__gen_max_x:float = 10
			self.__gen_min_y:float = -10
			self.__gen_max_y:float = 10
		else:
			self.__gen_min_x:float = x_min
			self.__gen_max_x:float = x_max
			self.__gen_min_y:float = y_min
			self.__gen_max_y:float = y_max

	def hasDataPoints(self) -> bool:
		"""
		Returns `true` if there are any stored `DataPoint`s.
		"""
		return self.__data_points.size() > 0

	def generateDataPoints(self, override:bool=False) -> None:
		"""
		Generates data points for the function contained in the\n
		`x` and `y` ranges.\n
		the data points can be accessed using `DataPointGenerator.getDataPoints()`.
		`override`: whether to forcibly recalculate ALL `DataPoint`s.
		"""
		print("Generating graph points...")
		# generate y values in the y range for x values in the x range.
		# the step between x values generated is dx.
		
		# we need arange because python decided it didnt like float ranges
		for x_i in tqdm(np.arange(self.__gen_min_x, self.__gen_max_x, self.__dx)):
			# if override is on, just generate the point with disregard to existence
			if (self.__data_points.getPointAtX(x_i) == None) or (override):
				returned_yval = self.__equation.evaluateEquation(x_i)

				if returned_yval != None: # this will happen if the number had an imaginary part
					self.__addDataPoint(DataPoint(x_i, returned_yval))

		print("Done!")

	def clearDataPoints(self) -> None:
		"""
		Clear all stored `DataPoint`s.\n
		"""
		self.__data_points.clearDataPoints()
			
if __name__ == "__main__":

	eq = Equation()
	# eq.askParser()
	eq.askParserEquation()
	# eq.askEquation()

	# tested with Cos[x]. adjusting bounds works correctly :)
	if (eq.hasStoredFunction()):

		dpg = DataPointGenerator(eq, x_min=-5, x_max=5, dx=0.001)
		dpg.generateDataPoints()
		
		dpl = dpg.getDataPoints()

		# dpl.forEach(lambda dp: y_list.append(dp.getY()))

		print("Data Points: {}".format(dpg.getDataPoints().size()))
		print("Clearing data points...")
		dpg.clearDataPoints()
		print("Data Points: {}".format(dpg.getDataPoints().size()))