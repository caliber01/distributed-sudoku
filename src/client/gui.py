import client.events as events
from common.listener import Listener, handler
import tkFont
from Tkinter import Tk, Toplevel
import client.ui.nickname as nickname
import client.ui.connect as connect
import client.ui.connecting as connecting
import client.ui.dashboard as dashboard
import client.ui.join_game as join_game
import client.ui.waiting_list as waiting_list
import common.protocol as protocol

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
        self.nickname_frame = None
        self.connect_frame = None
        self.connecting_msg = None
        self.dashboard_frame = None
        self.message = None
        self.waiting_frame = None

    def render_welcome(self):
        self._setup_font()
        self.nickname_frame = nickname.Nickname(master=self.root)
        self.nickname_frame.bind(nickname.SUBMIT, self._handle_nickname)

        self.root.after(100, self._check_events)
        self.root.mainloop()

    def render_join(self):
        self._setup_font()
        self.frame = join_game.Join(master=self.root)
        self.frame.bind(join_game.JOIN, self._connect)

    def _setup_font(self):
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        self.root.option_add("*Font", default_font)

    def _handle_nickname(self, event):
        self.out_queue.publish(events.SUBMIT_NICKNAME, self.nickname_frame.nickname)
        self.nickname_frame.destroy()
        self.connect_frame = connect.Connect(master=self.root)
        self.connect_frame.bind(connect.CONNECT, self._handle_connect)

    def _handle_connect(self, event):
        self.out_queue.publish(events.CONNECT_TO_SERVER, (self.connect_frame.address, int(self.connect_frame.port)))
        self.connecting_msg = connecting.Connecting('Connecting', 'Connecting to server...')

    def _check_events(self):
        try:
            self.handle_event(block=False)
        except Empty:
            pass
        self.root.after(100, self._check_events)

    def _handle_create_game(self, event):
        self.out_queue.publish(events.CREATE_ROOM, name=self.dashboard_frame.name, max_users=self.dashboard_frame.max_people)
        self.connecting_msg = connecting.Connecting('New game', 'Creating new game...')

    @handler(events.ERROR_CONNECTING_TO_SERVER)
    def error_connecting_to_server(self):
        self.connecting_msg.destroy()
        tkMessageBox.showerror("Connection error", "Error connecting to server")

    @handler(events.CONNECTED_TO_SERVER)
    def connected_to_server(self):
        self.connecting_msg.destroy()
        self.connect_frame.destroy()
        self.dashboard_frame = dashboard.Dashboard(master=self.root)
        self.dashboard_frame.bind(dashboard.CREATE_GAME, self._handle_create_game)

    @handler(events.ROOM_CREATED)
    def room_created(self, **room):
        self.connecting_msg.destroy()
        self.dashboard_frame.destroy()
        self.waiting_frame = waiting_list.WaitingList(self.root, room)

    @handler(protocol.PEOPLE_CHANGED)
    def people_changed(self, **kwargs):
        print(kwargs)
