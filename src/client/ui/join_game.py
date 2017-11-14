from Tkinter import *
import tkFont

JOIN_GAME = '<<join-game>>'

class Join(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=3)
        self.nickname = None

    def get_attributes(self):
        self.name = ['sud1', 'sud2']
        self.max = [5, 7]
        self.current = [3, 2]
        self.need = []
        for i in range(len(self.name)):
            self.need.append(self.max[i] - self.current[i])
        self.id = [43, 235]
        return (self.name, self.need, self.id)

    def create_widgets(self):
        #self._label = Label(self, text='Choose the game')
        #self._label.grid(row=0)

        name_game, number, id = self.get_attributes()

        self._game_list = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=True, xscrollcommand=True)
        for i in range(len(name_game)):
            self._game_list.insert(i, 'Game: ' + name_game[i] + ' (' + str(number[i]) + ' players are needed)')
        self._game_list.grid(row=2, ipadx=100, pady=15, padx=10)

        self._button_join = Button(self, text='Join to game', command=self.join)
        self._button_join.grid(row=4, pady=10)

    def join(self):
        self.index = int(self.Game_list.curselection()[0])
        self.id_game = id[self.index]
        self.event_generate(JOIN_GAME)


