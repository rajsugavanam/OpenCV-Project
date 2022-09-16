import sympy as sp
from sympy.abc import x

__cos_series = sp.series(sp.cos(x), x, 0, 4).removeO()
__sin_series = sp.series(sp.sin(x), x, 0, 4).removeO()

__tan_series = __sin_series/__cos_series

# ---------------------------------------------------------------------------- #
def fast_atan(input:float) -> float:
	"""
	Uses its power series expansion with fewer terms to
	approximate `arctan(x)`.
	"""
	# I use tangent because arctangent isn't convergent
	# __approximated_tan = sp.series(sp.tan(x), x, 0, 5)

	__solutions = sp.solveset(
		sp.Eq(__tan_series, input),
		x,
		domain=sp.Interval(-sp.pi/2, sp.pi/2)
	)
	# force solution to be within -pi/2 and pi/2
	# there will only be one solution in given interval
	for __solution in __solutions:
		return __solution

	return None
# ---------------------------------------------------------------------------- #
def fast_cos(input:float) -> float:
	"""
	Uses its power series expansion with fewer terms to
	approximate `cos(x)`. Optimized for -pi/2 to pi/2.
	"""
	__evaluated = __cos_series.evalf(6, subs={x:input})
	# __evaluated = __approximation.evalf(6, subs={x:input})
	return __evaluated
# ---------------------------------------------------------------------------- #
def fast_sin(input:float) -> float:
	"""
	Uses its power series expansion with fewer terms to
	approximate `sin(x)`. Optimized for -pi/2 to pi/2.
	"""
	__evaluated = __sin_series.evalf(6, subs={x:input})
	return __evaluated