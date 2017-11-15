from Tkinter import *
import tkFont
from client.ui.join_game import Join

CREATE_GAME = '<<create-game>>'

def validate_gamename(name):
    """
    validation of filling in game name form
    game name must contain only letters and underline
    """
    return bool(re.match(r'^[a-zA-Z0-9_]*$', name))

def validate_numberpeople(number):
    """
    validation of filling in number of needed players
    must contain only numbers, and the number must be less that 9
    """
    return not number or bool(re.match(r'^[1-8]+$', number)) and int(number) < 9

class Dashboard(Frame):

    def __init__(self, master=None, **kw):
        """
        creates an interface for the new user
        """
        Frame.__init__(self, master, **kw)
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        """
        creates 2 options for the user
        they can either create a new game or join the existing one
        """
        self.new_game_widgets()
        self.join_game_widgets()

    def new_game_widgets(self):
        """
        create a widget when user decides to create a new game
        a widget contains a form that needs to be filled to create a new game
        """
        self.new_game_lbl = Label(self, text = "New game")
        self.new_game_lbl.grid(row=0, column=0)

        self.left_frame = Frame(self, borderwidth=1, relief=SUNKEN)
        self.left_frame.grid(row=1, column=0, padx=20, pady=20, ipadx=20, ipady=10)

        self.name_lbl = Label(self.left_frame, text="Name:")
        self.name_lbl.grid(row=1, column=0, pady=20, padx=20)

        validate_gamename_command = self.register(validate_gamename)
        self.name_entry = Entry(self.left_frame, validate='all', validatecommand=(validate_gamename_command, '%P'))
        self.name_entry.grid(row=1, column=1, columnspan=2)

        self.max_people_lbl = Label(self.left_frame, text="Max people:")
        self.max_people_lbl.grid(row=2, column=0, pady=20, padx=20)

        validate_numberpeople_command = self.register(validate_numberpeople)
        self.max_people_entry = Entry(self.left_frame, validate='all', validatecommand=(validate_numberpeople_command, '%P'))
        self.max_people_entry.grid(row=2, column=1, columnspan=2, padx=10)

        self.create_game_btn = Button(self.left_frame, text="Create", command=self.create_game)
        self.create_game_btn.grid(row=3, column=1, pady=10)


    def join_game_widgets(self):
        """
        connects user to the game that the user chose to join
        """
        self.connect_lbl = Label(self, text = "Join game")
        self.connect_lbl.grid(row=0, column=3, columnspan=3)

        self.right_frame = Frame(self, borderwidth=1, relief=SUNKEN)
        self.right_frame.grid(row=1, column=3)

        self.join_frame = Join(self.right_frame)
        self.join_frame.grid(row=2, column=4)

    def create_game(self):
        """
        creates a new game when user filled the form and submitted it
        """
        self.name = self.name_entry.get()
        self.max_people = int(self.max_people_entry.get())
        self.event_generate(CREATE_GAME)


if __name__ == '__main__':
    root = Tk()
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=14)
    root.option_add("*Font", default_font)
    Dashboard(root)
    root.mainloop()
