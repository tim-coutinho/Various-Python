'''
	A program that uses a DFA (Deterministic Finite State Automaton)
	to determine if the given input is a valid double.
	Tim Coutinho
'''

import re
import sys
import numpy as np

transTable = np.array([[2,3,9,4],[2,9,6,5],[2,9,9,4],[5,9,9,9],
					   [5,9,6,9],[8,7,9,9],[8,9,9,9],[8,9,9,9],[9,9,9,9]])
valid = [2, 5, 8]

def hasInvalidAscii(d):
	return re.search(r'[^0-9eE\.\+-]', d)

def getDoubles():
	with open(sys.argv[1]) as f:
		lines = f.read().splitlines()
	return lines

def evaluate():
	for double in getDoubles():
		if hasInvalidAscii(double):
			state = 9
		else:
			state = evaluateDouble(1, double)
		print(double, 'A' if state in valid else 'R')

def evaluateDouble(state, double):
	if re.match(r'[0-9]', double):
		return evaluateDouble(transTable[state-1][0], double[1:])
	elif re.match(r'[\+-]', double):
		return evaluateDouble(transTable[state-1][1], double[1:])
	elif re.match(r'[eE]', double):
		return evaluateDouble(transTable[state-1][2], double[1:])
	elif re.match(r'\.', double):
		return evaluateDouble(transTable[state-1][3], double[1:])
	else:
		return state

evaluate()
