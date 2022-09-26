import sys
sys.path.append("../../")

from typing import Callable
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import T
from sympy.abc import x
from sympy import im, E
from graph_math.ParsingTypes import ParsingTypes

class Equation(object):
	"""
	Interfaces with the user to input an equation and parser.
	Holds a single function `f(x)` for evaluation.
	"""
	CONSTANTS = {
		"e": sp.E,
		"pi": sp.pi
	}
# ---------------------------------------------------------------------------- #
	def __init__(self, parser_type:ParsingTypes=None) -> None:
		self.__parser_type:ParsingTypes = parser_type
		self.__equation = None
		self.__derivative = None
# ---------------------------------------------------------------------------- #
	def getStoredFunction(self) -> Callable[[float], float]:
		"""
		Get the stored function `f(x)`.
		"""
		return self.__equation
# ---------------------------------------------------------------------------- #
	def hasStoredFunction(self) -> bool:
		"""
		Whether there is a stored function, `f(x)`.
		"""
		return self.__equation != None
# ---------------------------------------------------------------------------- #
	def getParser(self) -> ParsingTypes:
		"""
		Get the type of `ParsingTypes` currently set.
		"""
		return self.__parser_type
# ---------------------------------------------------------------------------- #
	def evaluateEquation(self, numInput:float) -> float:
		"""
		Plugs an input for `x` into the stored function `f(x)`.\n
		Returns: The output of the evaluated function.
		"""
		if self.__equation == None:
			print("Failed to evaluate equation: no equation found.")
			return None
		else:
			try:
				evaluated = self.__equation.subs(x, numInput)
				real = self.__removeImaginaryComp(evaluated)
				if (real != None):
					return real
			except:
				# things like factorial might have a pole error
				pass
			
			return None
# ---------------------------------------------------------------------------- #
	def evaluateDerivative(self, numInput:float) -> float:
		"""
		Plugs an input for `x` into the stored derivative of `f(x)`.\n
		Returns: The output of the evaluated derivative.
		"""
		if (self.__equation == None) or (self.__derivative == None):
			print(
				"Failed to evaluate derivative: no parent equation " +
				"or derivative found."
			)
			return None
		else:
			try:
				evaluated = self.__derivative.subs(x, numInput)
				real = self.__removeImaginaryComp(evaluated)
				if (real != None):
					return real
			except:
				pass
			
			return None
# ---------------------------------------------------------------------------- #
	def __removeImaginaryComp(self, complexNum:complex) -> complex:
		"""
		Returns none if the number is imaginary, but itself if there is no
		imaginary component.
		`complexNum`: the number to remove the imaginary part of.
		"""
		# if the output is imaginary, discard it
		if im(complexNum) != 0:
			return None
		else:
			return complexNum
# ---------------------------------------------------------------------------- #
	def askParserEquation(self) -> None:
		"""
		Prompts/reprompts the user for their choice of parser and equation,
		saving it to the Equation Object.\n
		This just uses `askParser()` and `askEquation()`.
		"""
		self.askParser()
		self.askEquation()
# ---------------------------------------------------------------------------- #
	def askEquation(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		"""
		if self.__parser_type == None:
			print("Cannot parse an equation without a parser selected!")

		else:
			while True:
				print(
					"\033[4mEnter your equation."
					+" You have the {} parser type selected.\033[0m"
					.format(self.__parser_type.name)
				)
				inputEq = input(
					"f(x)="
				)

				if self.__parser_type == ParsingTypes.MATHEMATICA:
					self.__equation = sp.simplify(
						parse_mathematica(inputEq)
					)

				elif self.__parser_type == ParsingTypes.LATEX:
					self.__equation = sp.simplify(
						parse_latex(inputEq)
					)

				self.__equation = self.__equation.doit()

				# only allowed variable will be `x`, so that's the variable
				# the derivative is respect to.
				#! i guess sympy really hates taking the derivative of |x|.
				#! you can probably just use sqrt(x^2) and call it a day.
				self.__derivative = sp.diff(
					self.__equation, x
				).doit()
				print(self.__derivative)

				self.__replaceEqAndDerivConstants()
				if self.__verifyFunctionVars():
					# function is now verified
					print("Parsed Equation:", self.__equation)
					break

				# at this point the user will have entered an invalid function
				print(
					"\nPlease write a function that simplifies to one that only contains the variable x."
				)
# ---------------------------------------------------------------------------- #
	def __replaceEqAndDerivConstants(self) -> None:
		"""
		Replaces constants for the stored equation and its derivative.
		"""
		self.__equation = self.__replaceConstants(self.__equation)
		self.__derivative = self.__replaceConstants(self.__derivative)
# ---------------------------------------------------------------------------- #
	def __replaceConstants(self, func):
		"""
		Replaces the equation constants defined under this class.
		"""
		for symbol in Equation.CONSTANTS:
			value = Equation.CONSTANTS[symbol]
			func = func.subs(symbol, value)

		return func
# ---------------------------------------------------------------------------- #
	# Verifies the variables of a function.
	# Returns: False if there is a variable other than x.
	def __verifyFunctionVars(self) -> bool:
		"""
		Verify that the entered function follows `f(x)`. That is, if it
		contains no other variables.
		Returns: `True` if the function's only variable is x.
		"""
		for var in self.__equation.free_symbols:
			if str(var) != "x": # x is from sympy.abc
				return False

		return True
# ---------------------------------------------------------------------------- #
	def askParser(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		"""
		print("\nBefore you input an equation, you need to select a specific")
		print("format to use. Which one of the following would you like to use?\n")

		print("Enter one of the following number keys to select a type.\n")

		print("[1] -- Mathematica/Wolfram Language\n")
		print("[2] -- LaTeX (requires the antlr4 Python package)\n")
		print("[exit] -- Cancel")

		while True:
			option_selection = input("\nSelection: ").lower().strip()

			if option_selection == "1": # 1
				self.__parser_type = ParsingTypes.MATHEMATICA
				break
			elif option_selection == "2": # 2
				self.__parser_type = ParsingTypes.LATEX
				break
			elif option_selection == "exit": # esc
				break
			else:
				print("Please enter a valid input.")
# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
	eqInp = Equation()

	eqInp.askParserAndEquation()

	fltInp = input("Enter an x value: ")
	print(eqInp.evaluateEquation(fltInp))