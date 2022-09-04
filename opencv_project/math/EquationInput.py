from math import pi
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica
from sympy.parsing.latex import parse_latex
from sympy.abc import x, y
import keyboard
import os
from ParsingTypes import ParsingTypes

#! TODO ADD COMMENTS
class EquationInput(object):

	def __init__(self):
		self.parser_type = None
		self.equation = None

	def getEquation(self):
		return self.equation

	def evaluateEquation(self, numInput):
		if self.equation == None:
			print("Failed to evaluate equation: no equation found.")
			return None
		else:
			return self.equation.evalf(6, subs={x:numInput})

	def askEquation(self):
		if self.parser_type == None:
			print("Cannot parse an equation without a parser selected!")

		else:
			while True:
				inputEq = input(
					"Enter your equation. You have the {} parser type selected.\n"
					.format(self.parser_type.name)
				)

				if self.parser_type == ParsingTypes.MATHEMATICA:
					self.equation = parse_mathematica(inputEq)

				elif self.parser_type == ParsingTypes.LATEX:
					self.equation = parse_latex(inputEq)

				if self.verifyFunctionVars():
					break

				# at this point the user will have entered an invalid function
				print(
					"\nPlease enter a function that only contains the variable x."
				)

		
	# Verifies the variables of a function.
	# Returns: False if there is a variable other than x.
	def verifyFunctionVars(self):
		for var in self.equation.free_symbols:
			if var != x: # x is from sympy.abc
				return False
		
		return True

	def askEquationParsingType(self):
		print("\nBefore you input an equation, you need to select a specific")
		print("format to use. Which one of the following would you like to use?\n")

		print("Enter one of the following number keys to select a type.\n")

		print("[1] -- Mathematica/Wolfram Language\n")
		print("[2] -- LaTeX\n")
		print("[exit] -- Cancel")

		while True:
			option_selection = input("\nSelection: ").lower().strip()

			if option_selection == "1": # 1
				self.parser_type = ParsingTypes.MATHEMATICA
				break
			elif option_selection == "2": # 2
				self.parser_type = ParsingTypes.LATEX
				break
			elif option_selection == "exit": # esc
				break
			else:
				print("Please enter a valid input.")

if __name__ == "__main__":
	eqInp = EquationInput()

	eqInp.askEquationParsingType()
	eqInp.askEquation()

	fltInp = input("Enter an x value: ")
	print(eqInp.evaluateEquation(fltInp))