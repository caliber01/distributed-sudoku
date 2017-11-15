from Tkinter import *
import tkFont
import client.sudoku as sudoku


class Board(Frame):


    def __init__(self, raw_matrix, on_edit_cell, master=None):
        """
        creates new game board
        """
        Frame.__init__(self, master)
        self.on_edit_cell = on_edit_cell
        self.grid(row=0, column=0)
        self.square_vars = {}
        self.matrix = sudoku.parse_grid(raw_matrix)
        self.create_widgets()


    def create_widgets(self):
        """
        creates 3x3 squares layout, each of squares has 3x3 layout on its own
        """
        rows = ['ABC', 'DEF', 'GHI']
        cols = ['123', '456', '789']
        subgrid_squares = [sudoku.product(rs, cs) for rs in rows for cs in cols]

        def validate_cell(cell):
            if cell == '':
                return True
            try:
                int(cell)
            except ValueError:
                return False
            return len(cell) == 1

        validate_command = self.register(validate_cell)

        for i in range(9):
            f = Frame(self, borderwidth=10, relief=GROOVE)
            for j in range(9):
                square = subgrid_squares[i][j]
                square_value = self.matrix[square]
                common_args = { 'justify': 'center', 'width': 4, 'fg': 'black', 'validate': 'all', 'validatecommand': (validate_command, '%P') }
                if square_value != '0':
                    e = Entry(f, **common_args)
                    e.insert(0, square_value)
                    e.config(state=DISABLED)
                else:
                    var = StringVar()
                    var.trace('w', self._get_cell_edit_handler(square))
                    self.square_vars[square] = var
                    e = Entry(f, textvariable=var, **common_args)
                e.grid(row=j // 3, column=j % 3, padx=5, pady=5, ipady=10)
            f.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def _get_cell_edit_handler(self, square):
        """
        if this user changes a cell, we call this function to update this cell for all other users
        """
        def handler(*args):
            self.on_edit_cell(square, int(self.matrix[square] or 0), int(self.square_vars[square].get() or 0))
            self.matrix[square] = int(self.square_vars[square].get() or 0)
        return handler

    def update_cell(self, x, y, value):
        """
        updates cell in this user's board if another user changes it
        """
        if value == 0:
            value = ''
        square = chr(x + ord('A')) + str(y+1)
        prev = self.square_vars[square].get() or 0
        if int(prev) == (value or 0):
            return
        self.matrix[square] = value
        self.square_vars[square].set(value)


full_matrix = """
4 8 3 9 2 1 6 5 7
9 6 7 3 4 5 8 2 1
2 5 1 8 7 6 4 9 3
5 4 8 1 3 2 9 7 6
7 2 9 5 6 4 1 3 8
1 3 6 7 9 8 2 4 5
3 7 2 6 8 9 5 1 4
8 1 4 2 5 3 7 6 9
6 9 5 4 1 7 3 8 2
"""

matrix_to_solve = """
0 0 3 0 2 0 6 0 0
9 0 0 3 0 5 0 0 1
0 0 1 8 0 6 4 0 0
0 0 8 1 0 2 9 0 0
7 0 0 0 0 0 0 0 8
0 0 6 7 0 8 2 0 0
0 0 2 6 0 9 5 0 0
8 0 0 2 0 3 0 0 9
0 0 5 0 1 0 3 0 0
"""

