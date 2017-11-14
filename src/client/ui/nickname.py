from Tkinter import *
import ttk
import tkMessageBox
import os

SUBMIT = '<<submit>>'

#GREETING = "Create or choose one"

def validate_gamename(name):
    return bool(re.match(r'^[a-zA-Z0-9_]*$', name))

class Nickname(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.nicks = set()
        #read unique nicknames from doc

        with open('nicknames.txt', 'w+') as file:
            for row in file:
                word = row.strip()
                if word not in self.nicks:
                    self.nicks.add(word)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)
        self.nickname = None

    def create_widgets(self):
        self._label = Label(self, text='Welcome to Sudoku game', font=4)
        self._label.grid(row=0, columnspan=2)

        self._label = Label(self, text='Create or choose nickname')
        self._label.grid(row=3, columnspan=2, rowspan=2)

        validate_gamename_command = self.register(validate_gamename)
        self._nickname = ttk.Combobox(self, state='normal', values=list(self.nicks), validate='all', validatecommand=(validate_gamename_command, '%P'))
        #self._nickname.set(GREETING)
        self._nickname.grid(row=5, ipadx=10, ipady=10, pady=10)

        self._button_continue = Button(self, text='Continue', command=self.submit)
        self._button_continue.grid(row=6, pady=20)

    def submit(self):
        name = self._nickname.get()
        if name == '':
            tkMessageBox.showinfo('Nickname', 'Please choose your nickname')
            return
        #write nickname only it is unique
        if name not in self.nicks:
            self.nicks.add(name)
            with open('nicknames.txt', "a") as f:
                f.write(os.linesep + name)

        self.nickname = name
        self.event_generate(SUBMIT)



