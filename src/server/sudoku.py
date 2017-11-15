from random import *


class Sudoku(object):

    def __solved(self):
        """
        creates 9x9 matrix filled with 1...9 numbers according to  sudoku rules
        """
        a = [[0 for x in range(9)] for y in range(9)]
        firstval = randint(1, 9)
        x = firstval
        v = 1
        for i in range(0, 9):
            for j in range(0, 9):
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

    def __unsolved(self, a, prob):
        """
        creates the copy of matrix from in __solved, and fills some cells with 0s with given probability
        """
        b = [[0 for x in range(9)] for y in range(9)]
        for i in range(0, 9):
            for j in range(0, 9):
                if (randint(1, 100) > prob * 100):
                    b[i][j] = a[i][j]
                else:
                    b[i][j] = 0
        return b

    def check(self, x, y, val):
        """
        checks if cell (x,y) in matrix has given value
        """
        return (self.solved[x][y] == val)

    def is_solved(self):
        """
        checks if unsolved matrix is filled with all the right values (and therefore, is solved)
        """
        return (self.solved == self.unsolved)


    def print_matrix(self):
        """
        printing matrix (for debugging)
        """
        return ''.join([''.join([str(item) for item in row]) for row in self.unsolved])

    def __str__(self):
        """
        returns string representation of matrix (string that contains 81 symbols, one for each cell)
        """
        s = ""
        for i in range(0, 9):
            for j in range(0, 9):
                s += str(self.unsolved[i][j])
        return s


    def __init__(self, prob=0.7):
        """
        creates new sudoku puzzle
        it contains 2 elements: solved (full) matrix
        and unsolved matrix, where some cells are filled with 0s according to given probability
        """
        self.solved = self.__solved()
        self.unsolved = self.__unsolved(self.solved, prob)
