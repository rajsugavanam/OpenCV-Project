from enum import Enum

class ParsingTypes(Enum):
	MATHEMATICA = 0
	"""
	Parses Wolfram Language.
	"""
	LATEX = 1
	"""
	Parses LaTeX. Requires the antlr4 Python package.
	"""