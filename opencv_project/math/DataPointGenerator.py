from opencv_project.math.Equation import Equation

class DataPointGenerator(object):

	def __init__(self) -> None:
		self.__equation = Equation()
		self.__data_points = []

		self.__gen_min_x = -10
		self.__gen_max_x = 10
		self.__gen_min_y = -10
		self.__gen_max_y = 10

		self.__dx = 0.001

	def getEquation(self) -> None:
		"""
		(`Equation`) Returns the stored equation.
		"""
		return self.__equation

	def getStoredFunction(self) -> function:
		"""
		(`lambda`) Returns the stored function `f(x)`.
		"""
		return self.__equation.getStoredFunction()

	def setDx(self, dx) -> None:
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

	def getDataPoints(self) -> list:
		"""
		Get the list of data points calculated for the function `f(x)`.\n
		Elements will be of the `DataPoint` type.
		"""
		return self.__data_points

	def setGenerationBoundX(self, minX, maxX) -> None:
		"""
		Set the `x` bound to generate values in.
		"""
		self.__gen_min_x = minX
		self.__gen_max_x = maxX

	def setGenerationBoundY(self, minY, maxY) -> None:
		"""
		Set the `y` bound to generate values in.
		"""
		self.__gen_min_y = minY
		self.__gen_max_y = maxY

	def generateDataPoints(self):
		# generate y values in the y range for x values in the x range.
		# the step between x values generated is dx.
		for x_i in range(self.__gen_min_x, self.__gen_max_x, self.__dx):
			returned_yval = self.__equation.evaluateEquation(x_i)
			