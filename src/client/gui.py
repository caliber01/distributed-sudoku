import client.events as events
from common.listener import Listener, handler
import tkFont
from Tkinter import Tk, Toplevel
import client.ui.nickname as nickname
import client.ui.connect as connect
import client.ui.connecting as connecting
import client.ui.dashboard as dashboard
from Queue import Empty
import tkMessageBox

import logging

logger = logging.getLogger(__name__)


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
        self.frame = None
        self.message = None

    def render_welcome(self):
        self._setup_font()
        self.frame = nickname.Nickname(master=self.root)
        self.frame.bind(nickname.SUBMIT, self._handle_nickname)

        self.root.after(100, self._check_events)
        self.root.mainloop()

    def _setup_font(self):
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        self.root.option_add("*Font", default_font)

    def _handle_nickname(self, event):
        self.frame.destroy()
        self.frame = connect.Connect(master=self.root)
        self.frame.bind(connect.CONNECT, self._handle_connect)

    def _handle_connect(self, event):
        self.out_queue.publish(events.CONNECT_TO_SERVER, (self.frame.address, int(self.frame.port)))
        self.connecting = connecting.Connecting()

    def _check_events(self):
        try:
            self.handle_event(block=False)
        except Empty:
            pass
        self.root.after(100, self._check_events)

    def _handle_create_game(self, event):
        self.out_queue.publish(events.CREATE_ROOM, name=self.frame.name, max_users=self.frame.max_people)

    @handler(events.ERROR_CONNECTING_TO_SERVER)
    def error_connecting_to_server(self):
        self.connecting.destroy()
        tkMessageBox.showerror("Connection error", "Error connecting to server")

    @handler(events.CONNECTED_TO_SERVER)
    def connected_to_server(self):
        self.connecting.destroy()
        self.frame.destroy()
        self.frame = dashboard.Dashboard(master=self.root)
        self.frame.bind(dashboard.CREATE_GAME, self._handle_create_game)
