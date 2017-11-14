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
import client.ui.board as board
import client.ui.result_board as result_board
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
        self.board_frame = None
        self.scores_frame = None
        self.session = {}

    def render_welcome(self):
        self._setup_font()
        self.nickname_frame = nickname.Nickname(master=self.root)
        self.nickname_frame.bind(nickname.SUBMIT, self._handle_nickname)

        self.root.after(100, self._check_events)
        self.root.mainloop()

    def _setup_font(self):
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        self.root.option_add("*Font", default_font)

    def _handle_nickname(self, event):
        self.out_queue.publish(events.SUBMIT_NICKNAME, self.nickname_frame.nickname)
        self.session['nickname'] = self.nickname_frame.nickname
        self.nickname_frame.destroy()
        self.connect_frame = connect.Connect(master=self.root)
        self.connect_frame.bind(connect.CONNECT, self._handle_connect)

    def _handle_connect(self, event):
        self.out_queue.publish(events.CONNECT_TO_SERVER, (self.connect_frame.address, int(self.connect_frame.port)))
        self.connecting_msg = connecting.Connecting('Connecting', 'Connecting to server...')

    def _handle_join(self, event):
        game_id = self.dashboard_frame.join_frame.game_id
        self.out_queue.publish(events.JOIN_GAME, game_id)
        self.connecting_msg = connecting.Connecting('Joining', 'Joinig to game...')

    def _leave_room(self, event):
        self.out_queue.publish(events.LEAVE_ROOM)

    def _check_events(self):
        try:
            self.handle_event(block=False)
        except Empty:
            pass
        self.root.after(1000, self._check_events)

    def _handle_create_game(self, event):
        self.out_queue.publish(events.CREATE_ROOM, name=self.dashboard_frame.name, max_users=self.dashboard_frame.max_people)
        self.connecting_msg = connecting.Connecting('New game', 'Creating new game...')

    # Notifications from logic.py

    @handler(events.ERROR_CONNECTING_TO_SERVER)
    def error_connecting_to_server(self):
        self.connecting_msg.destroy()
        tkMessageBox.showerror("Connection error", "Error connecting to server")

    @handler(events.CONNECTED_TO_SERVER)
    def connected_to_server(self):
        self.connecting_msg.destroy()
        self.connect_frame.destroy()
        self._show_dashboard()

    @handler(events.ROOM_LEAVED)
    def room_leaved(self):
        self.waiting_frame.destroy()
        self._show_dashboard()

    @handler(events.ROOMS_LOADED)
    def rooms_loaded(self, rooms):
        self.dashboard_frame.join_frame.update(rooms)

    @handler(events.ROOM_CREATED)
    def room_created(self, **room):
        self.connecting_msg.destroy()
        self.dashboard_frame.destroy()
        if self.board_frame:
            return
        self.waiting_frame = waiting_list.WaitingList(self.root, room, self.session['nickname'])
        self.waiting_frame.bind(waiting_list.LEAVE_ROOM, self._leave_room)

    @handler(events.ROOM_JOINED)
    def room_joined(self, **room):
        self.connecting_msg.destroy()
        self.dashboard_frame.destroy()
        self.waiting_frame = waiting_list.WaitingList(self.root, room, self.session['nickname'])
        self.waiting_frame.update_users(room["users"])
        self.waiting_frame.bind(waiting_list.LEAVE_ROOM, self._leave_room)

    # Notifications from server

    @handler(protocol.PEOPLE_CHANGED)
    def people_changed(self, **kwargs):
        if not self.waiting_frame:
            return
        self.waiting_frame.update_users(kwargs["users"])

    @handler(protocol.START_GAME)
    def start_game(self, **room):
        if self.connecting_msg:
            self.connecting_msg.destroy()
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        if self.waiting_frame:
            self.waiting_frame.destroy()
        self.board_frame = board.Board(room['matrix'], self.handle_edit_cell)

    def handle_edit_cell(self, square, prev_value, new_value):
        self.out_queue.publish(events.CELL_EDITED, square, prev_value, new_value)

    @handler(protocol.SUDOKU_CHANGED)
    def sudoku_changed(self, **change):
        self.board_frame.update_cell(change['x'], change['y'], change['value'])

    @handler(protocol.TOO_LATE)
    def too_late(self):
        tkMessageBox.showinfo("Damn it!", "You seem to be too late on this cell")

    @handler(protocol.SUDOKU_SOLVED)
    def sudoku_solved(self, scores, **kwargs):
        self.board_frame.destroy()
        self.scores_frame = result_board.ResultBoard(scores, self.root)
        self.scores_frame.bind(result_board.CLOSE, self._after_scores)

    def _after_scores(self, event):
        self.scores_frame.destroy()
        self._show_dashboard()
        self.out_queue.publish(events.GAME_ENDED)

    def _show_dashboard(self):
        self.dashboard_frame = dashboard.Dashboard(master=self.root)
        self.dashboard_frame.bind(dashboard.CREATE_GAME, self._handle_create_game)
        self.dashboard_frame.join_frame.bind(join_game.JOIN_GAME, self._handle_join)
        self.out_queue.publish(events.LOAD_ROOMS)

