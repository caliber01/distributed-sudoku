from Tkinter import *
import ttk

SUBMIT = '<<submit>>'


class Nickname(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.nicks = {'Bob', 'Alice', 'andr', 'z3jdv', '4uf', 'etrv'}
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)
        self.nickname = None

    def create_widgets(self):
        self._label = Label(self, text='Welcome to Sudoku game')
        self._label.grid(row=0, columnspan=2, rowspan=2)

        self._label = Label(self, text='')
        self._label.grid(row=2)

        self._nickname = ttk.Combobox(self, state='normal', values=list(self.nicks))
        self._nickname.set("Create or choose one")
        self._nickname.grid(row=3, ipadx=10, ipady=10)

        self._button_continue = Button(self, text='Continue', command=self.submit)
        self._button_continue.grid(row=4, pady=20)

    def submit(self):
        name = self._nickname.get()
        self.nicks.add(name)
        self.nickname = name
        self.event_generate(SUBMIT)



