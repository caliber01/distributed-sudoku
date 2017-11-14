from Tkinter import *
import tkFont

CREATE_GAME = '<<create-game>>'


class WaitingList(Frame):
    def __init__(self, master, room, nickname, **kw):
        Frame.__init__(self, master, **kw)
        self.room = room
        self.nickname = nickname

        self.users_var = StringVar()
        self.users_var.set(nickname)
        self.people_count_var = StringVar()
        self.people_count_var.set("(%d/%d)" % (1, self.room['max']))

        self.create_widgets()
        self.grid(row=0, column=0, padx=30, pady=30)

    def create_widgets(self):
        self.title_lbl = Label(self, text=self.room['name'])
        self.title_lbl.grid(row=0)

        self.lbl = Label(self, text="Waiting for more users before start...")
        self.lbl.config(font=("TkDefaultFont", 10))
        self.lbl.grid(row=1, pady=20)

        self.count_lbl = Label(self, textvariable=self.people_count_var)
        self.count_lbl.config(font=("TkDefaultFont", 12, 'bold'))
        self.count_lbl.grid(row=2)

        self.users_list = Listbox(self, listvariable=self.users_var)
        self.users_list.grid(row=3, pady=20, ipadx=10, ipady=10)

        self.leave_btn = Button(self, text="Leave")
        self.leave_btn.grid(row=4, pady=10)

    def update_users(self, users):
        self.room['users'] = users
        self.users_var.set(' '.join(users))
        self.people_count_var.set("(%d/%d)" % (len(users), self.room['max']))


if __name__ == '__main__':
    root = Tk()
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=14)
    root.option_add("*Font", default_font)
    WaitingList(root, 'Foo game')
    root.mainloop()
