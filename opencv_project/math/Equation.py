from EquationInput import EquationInput


class Equation(object):

	def __init__(self) -> None:
		self.__eq_input = EquationInput()

	def getStoredFunction(self):
		"""
		Returns: the stored function `f(x)`.
		"""
		return self.__eq_input.getStoredFunction()

	def hasStoredFunction(self):
		"""
		Returns: whether there is a stored function, `f(x)`.
		"""
		return self.__eq_input.hasStoredFunction()

	def askParserEquation(self) -> None:
		"""
		Prompts/reprompts the user for their choice of parser and equation,
		saving it to the Equation Object.\n
		This just uses `EquationInput.askParser()` and `EquationInput.askEquation()`.
		"""
		self.__eq_input.askParserAndEquation()

	def askEquation(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		See `EquationInput.askEquation()` for implementation.
		"""
		self.__eq_input.askEquation()

	def askParser(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		See `EquationInput.askParser()` for implementation.
		"""
		self.__eq_input.askParser()

	def evaluateEquation(self, input) -> float:
		"""
		Plugs an input for `x` into the stored function `f(x)`.\n
		See `EquationInput.evaluateEquation()` for implementation.\n
		Returns: (`float`) the output of the evaluated function.
		"""
		return self.__eq_input.evaluateEquation(input)
