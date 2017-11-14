from Tkinter import *
import ttk
import tkFont as tkfont


CLOSE = "<<close>>"


class ResultBoard(Frame):
    def __init__(self, scores, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self.nicks = sorted(scores, key=lambda player: player[1], reverse=True)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        bold_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
        small_font = tkfont.Font(family="Helvetica", size=11)
        self._label = Label(self, text=' Result Board ', font=bold_font)
        self._label.grid(row=0, rowspan=1, columnspan=2, sticky='n')

        self._label = Label(self, text=self.nicks[0][0] + " is the winner", font=small_font)
        self._label.grid(row=1, rowspan=1, columnspan=2, sticky='n')

        t1 = ''
        for i in range(0, len(self.nicks)):
            t1 += str(i + 1) + ".\t" + self.nicks[i][0] + "\t" + str(self.nicks[i][1]) + "\n"
        t2 = ''
        for i in range(0, len(self.nicks)):
            t2 += str(self.nicks[i][1]) + "\n"
        self._board1 = ttk.Label(self, text=t1, font=small_font)
        self._board1.grid(row=2, rowspan=1, column=0, columnspan=1, sticky='n')

        self._button_close = Button(self, text='Close', command=lambda *args: self.event_generate(CLOSE))
        self._button_close.grid(row=3)

