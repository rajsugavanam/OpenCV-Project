import sys
sys.path.append("../../")

from typing import Callable
from tqdm import tqdm

from opencv_project.math.DataPoint import DataPoint

class DataPointList(object):

	def __init__(self) -> None:
		self.data_points:dict[float, float] = {}

	def addOrChangeDataPoint(self, data_point:DataPoint) -> None:
		"""
		Add or change a `DataPoint` in the list.\n
		`data_point`: the point to add, update, or insert.
		"""
		self.data_points[data_point.getX()] = data_point.getY()

	def getPointAtX(self, x:float) -> DataPoint:
		"""
		Get the `DataPoint` of `f(x)` located at `x=<float>`.\n
		Returns: the corresponding `DataPoint` if there is an x value that is contained in one;
		else, `None`.
		"""
		# i use this so that an error isn't thrown
		# if the data point doesn't exist
		return self.data_points.get(x)

	def forEach(self, func:Callable[[DataPoint], None]) -> None:
		"""
		Run the given `Callable` consumer for each data point object.\n
		`func`: a function with format `func(float) -> None` to run with
		every data point.
		"""
		for x_i in tqdm(self.data_points):
			dp = DataPoint(x_i, self.data_points[x_i])
			func(dp)

	def clearDataPoints(self) -> None:
		"""
		Clear all stored `DataPoint`s.\n
		"""
		self.data_points.clear()

	def size(self) -> int:
		return len(self.data_points)