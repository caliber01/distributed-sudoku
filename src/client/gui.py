from Tkinter import *
import ttk
import client.events as events
from common.listener import Listener, handler


class UI(Listener):
    """
    Main class for user interface, runs in the main thread
    """

    def __init__(self, in_queue, out_queue):
        """
        :param in_queue: incoming messages queue
        :param out_queue: messages queue to publish events for ClientLogic
        """
        super(UI, self).__init__(in_queue)
        self.out_queue = out_queue

    def render_welcome(self):
        self.out_queue.publish(events.SUBMIT_NICKNAME, "Create nickname")

    @handler(events.ERROR_CONNECTING_TO_SERVER)

    def error_connecting_to_server(self, e):
        print(e)

def start_gui():

    global nicks, root
    nicks = ['Bob', 'Alice', 'andr', 'z3jdv', '4uf', 'etrv']
    root = Tk()
    root.title('Sudoku')
    root.geometry("400x350")
    New_nickname()

    root.mainloop()

class New_nickname():
    def __init__(self, master=None):



        self.label = Label(master, text='     Welcome to Sudoku game', font='sans 20')
        self.label.grid(row=0, columnspan=2, rowspan=2)

        self.label = Label(master, text='', font='sans 20')
        self.label.grid(row=2)

        self.nickname = ttk.Combobox(master, state='normal', values=list(set(nicks)))
        self.nickname.place(relx=0.2, rely=0.2, height=24, width=250)

        self.nickname.set("Create or choose one")

        def get_name():
            name = self.nickname.get()
            nicks.insert(0, name)
            print(nicks)
            print(name)

        self.button_create = Button(master, text='Get nickname', command=get_name)
        self.button_create.place(relx=0.3, rely=0.35, height=30, width=150)


if __name__ == '__main__':
    start_gui()