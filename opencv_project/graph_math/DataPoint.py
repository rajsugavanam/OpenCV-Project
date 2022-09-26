class DataPoint(object):
# ---------------------------------------------------------------------------- #
	def __init__(self, x:float, y:float) -> None:
		self.__x:float = x
		self.__y:float = y
# ---------------------------------------------------------------------------- #
	def __setX(self, x:float):
		"""
		Set the 'x'-value for this data point.
		"""
		self.__x = x
# ---------------------------------------------------------------------------- #
	def getX(self) -> float:
		"""
		Get the `x`-coordinate of the point.
		"""
		return self.__x
# ---------------------------------------------------------------------------- #
	def __setY(self, y:float):
		"""
		Set the 'y'-value for this data point.
		"""
		self.__y = y
# ---------------------------------------------------------------------------- #
	def getY(self) -> float:
		"""
		Get the `y`-value of the point.
		"""
		return self.__y
# ---------------------------------------------------------------------------- #
	def slopeWith(self, dp) -> float:
		"""
		Gets the slope between this data point and another given one.
		"""
		__slope = (dp.getY()-self.getY())/(dp.getX()-self.getX())
		return __slope