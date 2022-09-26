from os import system

import sys
sys.path.append("../../")

from graph_math.DataPointGenerator import DataPointGenerator
from graph_math.Equation import Equation
from graph_math.ParsingTypes import ParsingTypes
from visual.GraphIllustrator import GraphIllustrator
from visual.GraphImage import GraphImage

import numpy as np
import argparse
import cv2 as cv
import matplotlib


class GraphingCalculator(object):
	"""
	The main graphing calculator program.
	"""
	DIVIDER_LINE = "-------------------------------------------------------"
# ---------------------------------------------------------------------------- #
	def __init__(self) -> None:
		self.illustrator = None
		self.program_args = self.getProgramArgs()

		self.color = self.getArgumentColorOrDefault()
		self.thickness = self.getArgumentThicknessOrDefault()
# ---------------------------------------------------------------------------- #
	def getArgumentColorOrDefault(self):
		"""
		Gets a color value if specified in the arguments.
		"""
		if (self.program_args["color"] != None):
			rgb = matplotlib.colors.to_rgb(self.program_args["color"])
			return (rgb[2]*255, rgb[1]*255, rgb[0]*255)
		else:
			color = (0,255,0)
# ---------------------------------------------------------------------------- #
	def getArgumentThicknessOrDefault(self):
		"""
		Gets a thickness value if specified in the arguments.
		"""
		if (self.program_args["thickness"] != None):
			return self.program_args["thickness"]
		else:
			return 4
# ---------------------------------------------------------------------------- #
	def getProgramArgs(self) -> None:
		"""
		Uses an argument parser to get some essential arguments, like
		graph color and thickness.
		"""
		ap = argparse.ArgumentParser()
		ap.add_argument("--color", "-c", required=False, 
			help="A hex code representing the color of the graph.")
		ap.add_argument("--thickness", "-t", required=False, 
			help="An integer representing the graph's line thickness.")
		ap.add_argument("--width", "-w", required=True, 
			help="An integer representing the pixel width of the graph.")
		ap.add_argument("--length", "-l", required=True, 
			help="An integer representing the pixel length of the graph.")

		ap.add_argument("--xmin", required=True, 
			help="The lowest visible x of the graph.")
		ap.add_argument("--xmax", required=True, 
			help="The highest visible x of the graph.")
		ap.add_argument("--ymin", required=True, 
			help="The lowest visible y of the graph.")
		ap.add_argument("--ymax", required=True, 
			help="The highest visible y of the graph.")

		args = vars(ap.parse_args())

		return args
# ---------------------------------------------------------------------------- #
	def yesNoPrompt(self, string_prompt) -> bool:
		"""
		A simple yes/no prompt for the user with the given on-screen prompt.
		Returns whether they selected yes or no.
		"""
		while True:
			user_input = input(
				"\033[34;1m"
				+string_prompt
				+" (y/n)\033[0m "
			)
			if user_input.lower() == "y":
				return True
			elif user_input.lower() == "n":
				return False
			else:
				print("Please enter a valid option.")
# ---------------------------------------------------------------------------- #
	def askForGraphMask(self) -> None:
		eq2 = Equation(parser_type=ParsingTypes.LATEX)
		print(GraphingCalculator.DIVIDER_LINE)
		print("\033[92;1mMask equation:\033[0m")
		eq2.askEquation()
		print(GraphingCalculator.DIVIDER_LINE)
		masked = self.illustrator.maskedWithEquation(eq2)
		print(GraphingCalculator.DIVIDER_LINE)
		cv.imshow("Masked", masked)
# ---------------------------------------------------------------------------- #
	def mainGraph(self) -> None:
		"""
		Starts the main equation drawing sequence of this program.
		"""
		eq = Equation(parser_type=ParsingTypes.LATEX)

		print(GraphingCalculator.DIVIDER_LINE)

		print("\033[92;1mMain equation:\033[0m")
		eq.askEquation()

		print(GraphingCalculator.DIVIDER_LINE)

		dpg = DataPointGenerator(
			eq,
			x_min=int(self.program_args["xmin"]),
			x_max=int(self.program_args["xmax"]),
			y_min=int(self.program_args["ymin"]),
			y_max=int(self.program_args["ymax"])
		)

		dpg.generateDataPoints()


		self.illustrator = GraphIllustrator(
			int(self.program_args["width"]),
			int(self.program_args["length"]),
			dpg,
			self.color,
			self.thickness
		)
		self.illustrator.drawAxes()
		self.illustrator.drawGraph()
		self.illustrator.showLatexFunction()

		print(GraphingCalculator.DIVIDER_LINE)
# ---------------------------------------------------------------------------- #
	def graphImageSequence(self) -> None:
		"""
		Starts the Graph Image sequence of this program.
		Returns the `GraphImage` object for final use.
		"""
		# Graph image manipulation
		gimg = GraphImage(self.illustrator.getGraphImage())
		gimg.applySmoothing(3)
		gimg.showGraph()

		return gimg
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":

	program = GraphingCalculator()

	program.mainGraph()
	
	if program.yesNoPrompt("Would you like to enter a masking equation?"):
		program.askForGraphMask()

	gimg = program.graphImageSequence()

	if program.yesNoPrompt("Would you like to generate a histogram?"):
		gimg.showGraphHist()
	print(GraphingCalculator.DIVIDER_LINE)

	if program.yesNoPrompt("Would you like to save your incredible graph?"):
		gimg.saveGraph("saved_graph.jpg")
	
	cv.waitKey(0)