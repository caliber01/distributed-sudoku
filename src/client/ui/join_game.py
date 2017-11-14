from Tkinter import *
from common.protocol import GET_ROOMS

JOIN_GAME = '<<join-game>>'

class Join(Frame):
    def __init__(self, master=None, **kw):
        self.rooms = []
        self.id = []
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)
        self.nickname = None

    def update(self, rooms):
        self.rooms = rooms
        self._update_rooms_list()

    def _update_rooms_list(self):
        if self._game_list.size():
            self._game_list.delete(first=0, last=self._game_list.size())
            self.id = []
        i = 0
        for room in self.rooms:
            self._game_list.insert(i, 'Game ' + room["name"] + ' (players needed: ' + str(room["max"] - room["current"]) + ')')
            self.id.append(room["id"])
            i += 1


    def create_widgets(self):
        self._label = Label(self, text='Games', font='sans 16')
        self._label.grid(row=0, columnspan=2, rowspan=2)

        self._label = Label(self, text='')
        self._label.grid(row=2)

        self._game_list = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=True, xscrollcommand=True)
        self._update_rooms_list()
        self._game_list.grid(row=3, ipadx=35, ipady=20)

        self._button_join = Button(self, text='Join to game', command=self.join)
        self._button_join.grid(row=4, pady=20)

    def join(self):
        index = self._game_list.curselection()[0]
        self.game_id = self.id[index]
        self.event_generate(JOIN_GAME)


