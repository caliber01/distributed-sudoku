from Tkinter import *


class Connecting(Frame):
    def __init__(self, title, msg, **kw):
        """
        shows given message
        """
        self.top = Toplevel()
        self.top.title(title)
        Frame.__init__(self, self.top, **kw)
        self.pack()
        Message(self, text=msg, padx=40, pady=40, width=400).pack()

    def destroy(self):
        """
        removes message
        """
        Frame.destroy(self)
        self.top.destroy()
