from Tkinter import *


class Connect(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        self._main_label = Label(self, text='Dashboard')
        self._main_label.grid(row=0, columnspan=3)
