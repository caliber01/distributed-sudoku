import client.events as events
from common.listener import Listener, handler
import tkFont
from Tkinter import Tk
import client.ui.nickname as nickname
import client.ui.join_game as join_game
from Queue import Empty



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
        root = Tk()
        self.root = root
        root.title('Distributed Sudoku')

    def render_welcome(self):
        self._setup_font()
        self.frame = nickname.Nickname(master=self.root)
        self.frame.bind(nickname.SUBMIT, self._connect)

        self.root.after(100, self._check_events)
        self.root.mainloop()

    def render_join(self):
        self._setup_font()
        self.frame = join_game.Join(master=self.root)
        self.frame.bind(join_game.JOIN, self._connect)

        self.root.after(100, self._check_events)
        self.root.mainloop()

    def _setup_font(self):
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        self.root.option_add("*Font", default_font)

    def _connect(self, event):
        print(self.frame.nickname)

    def _check_events(self):
        try:
            self.handle_event(block=False)
        except Empty:
            pass
        self.root.after(100, self._check_events)

    @handler(events.ERROR_CONNECTING_TO_SERVER)
    def error_connecting_to_server(self, e):
        print(e)
