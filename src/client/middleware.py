import client.events as events
from common.queuelistener import QueueListener, handler
from threading import Thread, Event
from common.errors import *
import logging
from server.main import serve

logger = logging.getLogger(__name__)


QUIT = 'QUIT'


class Middleware(QueueListener):
    """
    Class to react on GUI events, call networking requests, notify GUI about new state
    Runs in separate thread
    """
    def __init__(self, requests_queue, gui_queue, host, server_type):
        """
        :param requests_queue: queue to subscribe to events (Subscription done in Listener baseclass)
        :param gui_queue: queue to publish events for GUI
        :param host: abstracted host
        """
        super(Middleware, self).__init__(requests_queue)
        self._gui_queue = gui_queue
        self._session = {}
        self._is_running = True
        self._server_type = server_type

        self._host = host
        self._thread = Thread(target=self._run)
        self._thread.start()
        self._server_thread = None
        self._server_shutdown_event = Event()

    def _run(self):
        """
        Run the Listener infinitely
        """
        while self._is_running:
            self.handle_queue_event(block=True)

    def shutdown(self):
        logger.info('Shutting down Logic')
        self.in_queue.publish(QUIT)
        self._host.shutdown()
        self._server_shutdown_event.set()

    @handler(QUIT)
    def quit(self):
        self._is_running = False

    @handler(events.SUBMIT_NICKNAME)
    def submit_nickname(self, nickname):
        self._session['nickname'] = nickname
        logger.info(nickname)

    @handler(events.CONNECT_TO_SERVER)
    def connect_to_server(self, server):
        self._session['server'] = server
        try:
            self._host.connect(server)
            self._host.set_name(self._session['nickname'])
        except Exception as e:
            logger.exception('Error connecting to server')
            self._gui_queue.publish(events.ERROR_CONNECTING_TO_SERVER)
            return
        self._gui_queue.publish(events.CONNECTED_TO_SERVER)

    @handler(events.HOST)
    def host_locally(self, server):
        self._server_thread = Thread(target=serve, args=(self._server_type,) + server + (self._server_shutdown_event,))
        self._server_thread.start()
        self.connect_to_server(server)

    @handler(events.LOAD_ROOMS)
    def load_rooms(self):
        try:
            rooms = self._host.load_rooms()
            self._gui_queue.publish(events.ROOMS_LOADED, rooms)
        except Exception as e:
            logger.exception('error loading rooms')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.JOIN_GAME)
    def join_game(self, id):
        try:
            game_info = self._host.join_game(id)
            if not game_info['started']:
                self._gui_queue.publish(events.ROOM_JOINED, **game_info)
        except Exception as e:
            logger.exception('error joining game')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.CREATE_ROOM)
    def create_room(self, name, max_users):
        try:
            room_details = self._host.create_room(name, max_users)
            print(room_details)
            logger.info('Room created')
            self._gui_queue.publish(events.ROOM_CREATED, **room_details)
        except Exception as e:
            logger.exception('error creating room')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.CELL_EDITED)
    def cell_edited(self, square, prev_value, new_value):
        x = ord(square[0]) - ord('A')
        y = int(square[1]) - 1
        try:
            self._host.cell_edited(x=x, y=y, prev_value=prev_value, new_value=new_value)
        except TooLateError:
            logger.exception('Error editing cell')
            self._gui_queue.publish(events.ERROR_TOO_LATE)
        except Exception:
            logger.exception('Error editing cell')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.LEAVE_ROOM)
    def leave_room(self):
        try:
            self._host.leave_room()
            self._gui_queue.publish(events.ROOM_LEAVED)
        except Exception as e:
            logger.exception('nrror leaving room')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.GAME_ENDED)
    def game_ended(self):
        pass
