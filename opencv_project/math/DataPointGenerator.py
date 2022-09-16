import sys
from typing import Callable

sys.path.append("../../")

import numpy as np
import sympy as sp

from tqdm import tqdm

from sympy.calculus.util import continuous_domain
from sympy.calculus.util import diff

from sympy.abc import x

from opencv_project.math.Equation import Equation
from opencv_project.math.FastMath import fast_atan, fast_cos
from opencv_project.math.DataPoint import DataPoint
from opencv_project.math.DataPointList import DataPointList

class DataPointGenerator(object):
	"""
	Generates data points from a given equation.
	"""

	DEFAULT_DX = 0.1
# ---------------------------------------------------------------------------- #
	def __init__(self, equation:Equation, 
		x_min:float=-10, x_max:float=10, 
		y_min:float=-10, y_max:float=10) -> None:
		self.__equation:Equation = equation
		self.__data_points:DataPointList = DataPointList()

		self.__fixEnteredBounds(x_min, x_max, y_min, y_max)

		# scale user value by range:
		# the larger the range, the smaller the dx
		self.__dx = 0.001*self.getXRange()
		# self.__dx = self.__dx*self.getXRange()/5
		
# ---------------------------------------------------------------------------- #
	def getEquation(self) -> Equation:
		"""
		(`Equation`) Returns the stored equation.
		"""
		return self.__equation
# ---------------------------------------------------------------------------- #
	def getStoredFunction(self) -> Callable[[float], float]:
		"""
		(`function`) Returns the stored function `f(x)`.
		"""
		return self.__equation.getStoredFunction()
# ---------------------------------------------------------------------------- #
	def setDx(self, dx:float) -> None:
		"""
		Set the value for `dx`. this is the delta between x values\n
		(or the spacing) between the `x` data points.
		"""
		self.__dx = dx
# ---------------------------------------------------------------------------- #
	def getDx(self) -> float:
		"""
		Get the value for `dx`. this is the delta between x values\n
		(or the spacing) between the `x` data points.
		"""
		return self.__dx
# ---------------------------------------------------------------------------- #
	def getDataPoints(self) -> DataPointList:
		"""
		Get the list of data points calculated for the function `f(x)`.\n
		"""
		return self.__data_points
# ---------------------------------------------------------------------------- #
	def __addDataPoint(self, data_point:DataPoint) -> None:
		"""
		Add a `DataPoint` to the generator's list.
		"""
		self.__data_points.addOrChangeDataPoint(data_point)
# ---------------------------------------------------------------------------- #
	def getXRange(self) -> float:
		"""
		Get the `x`-range represented by the bounds.\n
		Returns: The range of the `x` bounds.
		"""
		return self.__gen_max_x - self.__gen_min_x
# ---------------------------------------------------------------------------- #
	def getYRange(self) -> float:
		"""
		Get the `y`-range represented by the bounds.\n
		Returns: The range of the `y` bounds.
		"""
		return self.__gen_max_y - self.__gen_min_y
# ---------------------------------------------------------------------------- #
	def getXRange(self) -> float:
		"""
		Get the `x`-range represented by the bounds.\n
		Returns: The range of the `x` bounds.
		"""
		return self.__gen_max_x - self.__gen_min_x
# ---------------------------------------------------------------------------- #
	def getMinX(self) -> float:
		"""
		Get the lower `x` bound.\n
		"""
		return self.__gen_min_x
# ---------------------------------------------------------------------------- #
	def getMaxX(self) -> float:
		"""
		Get the upper `x` bound.\n
		"""
		return self.__gen_max_x
# ---------------------------------------------------------------------------- #
	def getMinY(self) -> float:
		"""
		Get the lower `y` bound.\n
		"""
		return self.__gen_min_y
# ---------------------------------------------------------------------------- #
	def getMaxY(self) -> float:
		"""
		Get the upper `y` bound.\n
		"""
		return self.__gen_max_y
# ---------------------------------------------------------------------------- #
	def getZeroXOffset(self) -> float:
		"""
		Get the `x` value representing the x-offset of the origin to the center.
		"""
		# multiply the average by negative to get the dist for the x origin to offset
		mid_x = -1*(self.__gen_max_x+self.__gen_min_x)/2
		# mid_x will be the distance to zero
		return mid_x
# ---------------------------------------------------------------------------- #
	def getZeroYOffset(self) -> float:
		"""
		Get the `y` value representing the x-offset of the origin to the center.
		"""
		# multiply the average by negative to get the dist for the x origin to offset
		mid_y = (self.__gen_max_y+self.__gen_min_y)/2
		# mid_x will be the distance to zero
		return mid_y
# ---------------------------------------------------------------------------- #
	def setGenerationBoundX(self, min_x:float, max_x:float, generate:bool=True) -> None:
		"""
		Set the `x` bound to generate values in.\n
		`min_x`: The minimum `x` value to generate points in.\n
		`max_x`: The maximum `x` value to generate points in.\n
		`generate`: Whether to generate additional points if the bound was expanded.
		"""
		if (self.__boundValid(min_x, max_x)):
			expanded:bool = self.__boundExpanded(min_x, self.__gen_min_x, 
				self.__gen_max_x, max_x)

			self.__gen_min_x = min_x
			self.__gen_max_x = max_x

			if generate and expanded:
				self.generateDataPoints()
		else:
			print("The lower X bound must be higher than the higher X bound. " +
				"\nBound was not set.")
# ---------------------------------------------------------------------------- #
	def setGenerationBoundY(self, min_y:float, max_y:float, 
		generate:bool=True) -> None:
		"""
		Set the `y` bound to generate values in.\n
		`min_y`: The minumum `y` value to generate points in.\n
		`max_y`: The maximum `y` value to generate points in.\n
		`generate`: Whether to generate additional points if the bound was expanded.
		"""
		if (self.__boundValid(min_y, max_y)):
			expanded:bool = self.__boundExpanded(min_y, self.__gen_min_y, self.__gen_max_y, max_y)

			self.__gen_min_y = min_y
			self.__gen_max_y = max_y

			if generate and expanded:
				self.generateDataPoints()
		else:
			print("The lower Y bound must be higher than the higher Y bound. " +
				"\nBound was not set.")
# ---------------------------------------------------------------------------- #
	def __boundExpanded(self, low:float, current_low:float, 
		current_high:float, high:float) -> bool:

		return (low < current_low) or (current_high > high)
# ---------------------------------------------------------------------------- #
	def __boundValid(self, min_val:float, max_val:float) -> bool:
		return (min_val<max_val)
# ---------------------------------------------------------------------------- #
	def __fixEnteredBounds(self, x_min:float, x_max:float, 
		y_min:float, y_max:float) -> None:
		"""
		Verify the bounds entered for this class. If any are invalid, the bounds
		will revert to their defaults.\n
		`x-min`: The desired minimum x bound.
		`x-max`: The desired maximum x bound.
		`y-min`: The desired mininum y bound.
		`y-max`: The desired maximum y bound.
		"""
		if (self.__boundValid(x_min, x_max) and self.__boundValid(y_min, y_max)) == False:
			print("The lower bounds must be higher than the higher bounds." +
				"Reverting to default value.")
			self.__gen_min_x:float = -10
			self.__gen_max_x:float = 10
			self.__gen_min_y:float = -10
			self.__gen_max_y:float = 10
		else:
			self.__gen_min_x:float = x_min
			self.__gen_max_x:float = x_max
			self.__gen_min_y:float = y_min
			self.__gen_max_y:float = y_max
# ---------------------------------------------------------------------------- #
	def isDiscontinuous(self, x1:float, x2:float) -> bool:
		"""
		Check if the stored function `f(x)` is discontinuous over the given interval.
		from `x1` and `x2`.\n
		`x1`: The left-side of the interval.\n
		`x2`: The right-side of the interval.\n
		Returns: Whether the function is discontinuous over the interval.
		"""
		interval = sp.Interval(x1, x2)
		return self.__doesIntervalIntersectDiscontinuity(interval)
# ---------------------------------------------------------------------------- #
	def __doesIntervalIntersectDiscontinuity(self, input_interval:sp.Interval) -> bool:
		"""
		Check if the stored function `f(x)` is discontinuous over the given interval.
		from `x1` and `x2`.\n
		`input_interval`: The given interval.\n
		Returns: Whether the function is discontinuous over the interval.
		"""
		#* handling discontinuities was easily 
		#* the most hardest part of this but i did it :)

		contDomain = continuous_domain(self.getStoredFunction(), x, input_interval)
		# if there isn't a continuous domain on the function that matches the two
		# x values, that means the function was discontinuous over the interval.
		return contDomain != input_interval
		# return (input_interval in interval) == False
# ---------------------------------------------------------------------------- #
	def hasDataPoints(self) -> bool:
		"""
		Returns `true` if there are any stored `DataPoint`s.
		"""
		return self.__data_points.size() > 0

# ---------------------------------------------------------------------------- #
	def __valueInYRange(self, y_value:float) -> bool:
		return self.__gen_min_y<=y_value<=self.__gen_max_y
# ---------------------------------------------------------------------------- #
	def generateDataPoints(self, override:bool=False) -> None:
		"""
		Generates data points for the function contained in the\n
		`x` and `y` ranges.\n
		the data points can be accessed using `DataPointGenerator.getDataPoints()`.\n
		`override`: whether to forcibly recalculate ALL `DataPoint`s.
		"""
		print("Generating graph points...")
		# generate y values in the y range for x values in the x range.
		# the step between x values generated is dx.
		# TODO IMPLEMENT ABOVE
		
		# we need arange because python decided it didnt like float ranges
		x_i = self.__gen_min_x
		while (x_i <= self.__gen_max_x):
		# for x_i in tqdm(np.arange(self.__gen_min_x, self.__gen_max_x, self.__dx)):
			# change dx based on how steep the derivative is at the given point.
			# this would make graphs like cot(x)/4 look better.
			
			# if override is on, just generate the point with disregard to existence			
			if (self.__data_points.getPointAtX(x_i) == None) or (override):
				returned_yval = self.__equation.evaluateEquation(x_i)

				# `None` will happen if the number had an imaginary part
				if returned_yval != None and self.__valueInYRange(returned_yval):
					self.__addDataPoint(DataPoint(x_i, returned_yval))
			
			__derivative_value = self.getEquation().evaluateDerivative(x_i)
			__new_dx = self.__getNewDx(__derivative_value)
			x_i += __new_dx

		print("Done!")
# ---------------------------------------------------------------------------- #
	def __getNewDx(self, derivative_value:float) -> float:
		MIN_DX = 0.1*self.__dx
		MAX_DX = 100*self.__dx
		if derivative_value != None:
			# if derivative isn't pi/2 or 3pi/2 etc
			__theta = sp.atan(derivative_value)
			# __theta = fast_atan(derivative_value)
			# will be a scale value between 0 and 1
			__dx_scale = fast_cos(__theta)
			__scaled_dx = __dx_scale*self.__dx
			__bounded_dx = max(min(__scaled_dx, MAX_DX), MIN_DX)
			return __bounded_dx
		else:
			# if not differentiable
			return self.__dx
# ---------------------------------------------------------------------------- #
	def checkDerivative(self, dp1, dp2, derivative_forgiveness:float=1):
		"""
		Checks whether `f(x)`'s derivative at `dp1` is close enough to the slope
		between `dp1` and `dp2`.
		"""
		pass
# ---------------------------------------------------------------------------- #
	def __checkDerivative(self, x1, x2):
		"""
		
		"""
		pass
# ---------------------------------------------------------------------------- #
	def clearDataPoints(self) -> None:
		"""
		Clear all stored `DataPoint`s.\n
		"""
		self.__data_points.clearDataPoints()
# ---------------------------------------------------------------------------- #

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