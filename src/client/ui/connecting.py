from Tkinter import *


class Connecting(Frame):
    def __init__(self, **kw):
        self.top = Toplevel()
        self.top.title('Connecting')
        Frame.__init__(self, self.top, **kw)
        self.pack()
        Message(self, text="Connecting to server...", padx=40, pady=40, width=400).pack()

    def destroy(self):
        Frame.destroy(self)
        self.top.destroy()
