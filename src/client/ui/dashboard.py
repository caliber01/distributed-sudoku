from Tkinter import *


class Dashboard(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        self.left_frame = Frame(self, relief=RIDGE)
        self.left_frame.grid(row=0, column=0)

        self.new_game_lbl = Label(self.left_frame, text = "New game")
        self.new_game_lbl.grid(row=0)

        self.right_frame = Frame(self, relief=RIDGE)
        self.right_frame.grid(row=0, column=1)

        self.connect_lbl = Label(self.right_frame, text = "Join game")
        self.connect_lbl.grid(row=0)
