import client.events as events
from common.queuelistener import QueueListener, handler
from threading import Thread, Event
import logging

logger = logging.getLogger(__name__)


class Middleware(QueueListener):
    """
    Class to react on GUI events, call networking requests, notify GUI about new state
    Runs in separate thread
    """
    def __init__(self, requests_queue, gui_queue, host):
        """
        :param requests_queue: queue to subscribe to events (Subscription done in Listener baseclass)
        :param gui_queue: queue to publish events for GUI
        :param host: abstracted host
        """
        super(Middleware, self).__init__(requests_queue)
        self._gui_queue = gui_queue
        self._session = {}

        self._host = host
        self._shutdown_event = Event()
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _run(self):
        """
        Run the Listener infinitely
        """
        while not self._shutdown_event.is_set():
            self.handle_queue_event(block=True)

    def shutdown(self):
        logger.info('Shutting down Logic')
        self._host.shutdown()
        self._shutdown_event.set()

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
            logger.error(e)
            self._gui_queue.publish(events.ERROR_CONNECTING_TO_SERVER)
            return
        self._gui_queue.publish(events.CONNECTED_TO_SERVER)

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
            self._host.cell_edited(x=x, y=y, prev=prev_value, value=new_value)
        except Exception as e:
            logger.exception('error editing cell')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.LEAVE_ROOM)
    def leave_room(self):
        try:
            self._host.leave_room()
            self._gui_queue.publish(events.ROOM_LEAVED)
        except Exception as e:
            logger.exception('error leaving room')
            self._gui_queue.publish(events.ERROR_OCCURRED)

    @handler(events.GAME_ENDED)
    def game_ended(self):
        pass
