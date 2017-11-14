from random import *

class Sudoku(object):
	solved = None
	unsolved = None
		
	def solved():
		a = [[0 for x in range(9)] for y in range(9)] 
		firstval = randint(1, 9)  
		x = firstval
		v = 1
		for i in range(0,9):
			for j in range(0,9):
				a[i][j] = (j + x + v) % 9 + 1
			x += 3
			if (x >= 9): x = x - 9
			if (i == 2):
				v = 2
				x = firstval
			if (i == 5):
				v = 3
				x = firstval
		return a
	
	def unsolved(a, prob):
		b = [[0 for x in range(9)] for y in range(9)] 
		for i in range(0,9):
			for j in range(0,9):
				if(randint(1,100) > prob*100): b[i][j] = a[i][j]
				else: b[i][j] = 0
		return b
		
	def check (self, x, y, val):
		return (self.solved[x][y] == val)
	
	def is_solved(self):
		return(self.solved == self.unsolved)
		
	def print_matrix(A):
		print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
			for row in A]))
			
	def __str__(self):
		s = ""
		for i in range(0,9):
			for j in range(0,9):
				s += str(self.unsolved[i][j])
		return s
			
	def __init__(self, prob = 0.7):
		self.solved = Sudoku.solved()
		self.unsolved = Sudoku.unsolved(self.solved, prob)