class DataPoint(object):

	def __init__(self, x, y) -> None:
		self.__x = x
		self.__y = y

	def getX(self):
		"""
		Get the `x`-coordinate of the point.
		"""
		return self.__x

	def getY(self):
		"""
		Get the `y`-value of the point.
		"""
		return self.__y