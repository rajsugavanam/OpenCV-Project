import sys
sys.path.append("../../")

from typing import Callable
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import T
from sympy.abc import x
from sympy import im, simplify
from sympy.calculus.util import continuous_domain
from opencv_project.math.ParsingTypes import ParsingTypes

class Equation(object):

	def __init__(self, parser_type:ParsingTypes=None) -> None:
		self.__parser_type:ParsingTypes = parser_type
		self.__equation = None

	def getStoredFunction(self) -> Callable[[float], float]:
		"""
		Returns: the stored function `f(x)`.
		"""
		return self.__equation

	def hasStoredFunction(self):
		"""
		Returns: whether there is a stored function, `f(x)`.
		"""
		return self.__equation != None

	def getParser(self) -> ParsingTypes:
		return self.__parser_type

	def evaluateEquation(self, numInput:float) -> float:
		"""
		Plugs an input for `x` into the stored function `f(x)`.\n
		Returns: (`float`) the output of the evaluated function.
		"""
		if self.__equation == None:
			print("Failed to evaluate equation: no equation found.")
			return None
		else:
			evaluated = self.__equation.evalf(6, subs={x:numInput})
			
			if im(evaluated) != 0:
				return None
			else:
				return evaluated

	def askParserEquation(self) -> None:
		"""
		Prompts/reprompts the user for their choice of parser and equation,
		saving it to the Equation Object.\n
		This just uses `askParser()` and `askEquation()`.
		"""
		self.askParser()
		self.askEquation()

	def askEquation(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		"""
		if self.__parser_type == None:
			print("Cannot parse an equation without a parser selected!")

		else:
			while True:
				inputEq = input(
					"\nEnter your equation. You have the {} parser type selected.\nf(x)="
					.format(self.__parser_type.name)
				)

				if self.__parser_type == ParsingTypes.MATHEMATICA:
					self.__equation = simplify(parse_mathematica(inputEq), transformations=T[4]).doit()

				elif self.__parser_type == ParsingTypes.LATEX:
					self.__equation = simplify(parse_latex(inputEq), transformations=T[4])

				if self.__verifyFunctionVars():
					# function is now verified
					break

				
				# at this point the user will have entered an invalid function
				print(
					"\nPlease write a function that simplifies to one that only contains the variable x."
				)
			
		
	# Verifies the variables of a function.
	# Returns: False if there is a variable other than x.
	def __verifyFunctionVars(self) -> bool:
		"""
		Verify that the entered function follows `f(x)`. That is, that it
		contains no other variables.
		Returns: (`bool`) `True` if the function's only variable is x.
		"""
		for var in self.__equation.free_symbols:
			if var != x: # x is from sympy.abc
				return False
		
		return True

	def askParser(self) -> None:
		"""
		Prompts/reprompts the user ONLY for their equation. Will fail if no parser
		is already selected.\n
		See `EquationInput.askParser()` for implementation.
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

if __name__ == "__main__":
	eqInp = Equation()

	eqInp.askParserAndEquation()

	fltInp = input("Enter an x value: ")
	print(eqInp.evaluateEquation(fltInp))