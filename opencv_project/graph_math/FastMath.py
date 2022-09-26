import sympy as sp
from sympy.abc import x

class fast_math(object):
	"""
	Contains trig functions that are computationally faster than their original
	counterparts, with the tradeoff of severe inaccuracy outside their optimized
	interval.

	See https://www.desmos.com/calculator/lsvyyvu2iz.
	"""
	__cos_series = sp.series(sp.cos(x), x, 0, 3).removeO()
	__sin_series = sp.series(sp.sin(x), x, 0, 3).removeO()
	__fast_arctan = (4/3)*sp.tanh((3*x/5))

	# ---------------------------------------------------------------------------- #
	@staticmethod
	def fast_atan(input:float) -> float:
		"""
		Uses a transformed hyperbolic tangent function to approximate `arctan(x)`.
		Works for all real `x` values.
		"""
		# I use tangent because arctangent isn't convergent
		# __approximated_tan = sp.series(sp.tan(x), x, 0, 5)
		__evaluated = fast_math.__fast_arctan.subs(x, input)
		return __evaluated
	# ---------------------------------------------------------------------------- #
	@staticmethod
	def fast_cos(input:float) -> float:
		"""
		Uses its power series expansion with fewer terms to
		approximate `cos(x)`. Only effective for the domain -pi/2 to pi/2.
		"""
		__evaluated = fast_math.__cos_series.subs(x, input)
		# __evaluated = __approximation.evalf(6, subs={x:input})
		return __evaluated
	# ---------------------------------------------------------------------------- #
	@staticmethod
	def fast_sin(input:float) -> float:
		"""
		Uses its power series expansion with fewer terms to
		approximate `sin(x)`. Only effective for the domain -pi/2 to pi/2.
		"""
		__evaluated = fast_math.__sin_series.subs(x, input)
		return __evaluated