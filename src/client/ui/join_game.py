from Tkinter import *
import ttk

JOIN = '<<join>>'


class Join(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)
        self.nickname = None

    def get_attributes(self):
        self.name = ['sud1', 'sud2']
        self.max = [5, 7]
        self.current = [3, 2]
        self.need = []
        for i in range(len(self.name)):
            self.need.append(self.max[i] - self.current[i])
        id = [43, 235]
        return (self.name, self.need, self.id)

    def create_widgets(self):
        self._label = Label(self, text='Games', font='sans 16')
        self._label.grid(row=0, columnspan=2, rowspan=2)

        self._label = Label(self, text='')
        self._label.grid(row=2)
        name_game, number, id = self.get_attributes()

        self._game_list = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=True, xscrollcommand=True)
        for i in range(len(name_game)):
            self._game_list.insert(i, 'Game: ' + name_game[i] + ' (' + str(number[i]) + ' players are needed)')
        self._game_list.grid(row=3, ipadx=35, ipady=20)

        self._button_join = Button(self, text='Join to game', command=self.join)
        self._button_join.grid(row=4, pady=20)

    def join(self):
        self.index = int(self.Game_list.curselection()[0])
        self.id_game = id[self.index]
        self.event_generate(JOIN)



