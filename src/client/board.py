from Tkinter import *
import tkFont
import client.sudoku as sudoku


class Board(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def create_widgets(self, matrix):
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

        print(subgrid_squares)
        for i in range(9):
            f = Frame(self, borderwidth=10, relief=GROOVE)
            for j in range(9):
                e = Entry(f, justify='center', width=4, fg='black', validate='all', validatecommand=(validate_command, '%P'))
                square_value = matrix[subgrid_squares[i][j]]
                if square_value != '0':
                    e.insert(0, square_value)
                    e.config(state=DISABLED)
                e.grid(row=j // 3, column=j % 3, padx=10, pady=10, ipady=20)
            f.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def __init__(self, matrix, master=None):
        Frame.__init__(self, master)
        self.create_widgets(matrix)
        self.grid(row=0, column=0)


root = Tk()
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=14)
root.option_add("*Font", default_font)

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

matrix = sudoku.parse_grid(matrix_to_solve)

app = Board(matrix, master=root)
app.mainloop()
root.destroy()

