from Tkinter import *
from common.protocol import GET_ROOMS

JOIN_GAME = '<<join-game>>'

class Join(Frame):
    def __init__(self, master=None, **kw):
        self.rooms = []
        self.id = []
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=3)
        self.nickname = None

    def update_rooms(self, rooms):
        self.rooms = rooms
        self._update_rooms_list()

    def _update_rooms_list(self):
        if self._rooms_list.size():
            self._rooms_list.delete(first=0, last=self._rooms_list.size())
            self.id = []
        for room in self.rooms:
            self._rooms_list.insert(END, 'Game ' + room["name"] + ' (players needed: ' + str(room["max"] - room["current"]) + ')')
            self.id.append(room["id"])


    def create_widgets(self):
        self._label = Label(self, text='')
        self._label.grid(row=2)

        self._rooms_list = Listbox(self, height=5, selectmode=SINGLE, yscrollcommand=True, xscrollcommand=True)
        self._update_rooms_list()
        self._rooms_list.grid(row=2, ipadx=100, pady=15, padx=10)

        self._button_join = Button(self, text='Join to game', command=self.join)
        self._button_join.grid(row=4, pady=10)

    def join(self):
        index = self._rooms_list.curselection()[0]
        self.game_id = self.id[index]
        self.event_generate(JOIN_GAME)


