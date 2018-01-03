import client.events as events
import common.protocol as protocol
from common.listener import Listener, handler
from threading import Thread
import logging

logger = logging.getLogger(__name__)


class ClientLogic(Listener):
    """
    Class to react on GUI events, call networking requests, notify GUI about new state
    Runs in separate thread
    """
    def __init__(self, in_queue, out_queue, connection):
        """
        :param in_queue: queue to subscribe to events (Subscription done in Listener baseclass)
        :param out_queue: queue to publish events for GUI
        :param connection: abstracted connection
        """
        super(ClientLogic, self).__init__(in_queue)
        self._out_queue = out_queue
        self._session = {}

        self._is_running = True
        self._thread = Thread(target=self.run)
        self._thread.start()
        self._connection = connection

    def run(self):
        """
        Run the Listener infinitely
        """
        while self._is_running:
            self.handle_event(block=True)

    @handler(events.QUIT)
    def quit(self):
        logger.info('Shutting down Logic')
        self._connection.shutdown()
        self._is_running = False

    @handler(events.SUBMIT_NICKNAME)
    def submit_nickname(self, nickname):
        self._session['nickname'] = nickname
        logger.info(nickname)

    @handler(events.CONNECT_TO_SERVER)
    def connect_to_server(self, server):
        self._session['server'] = server
        try:
            self._connection.connect(server)
            self.__set_name_request()
        except Exception as e:
            logger.error(e)
            self._out_queue.publish(events.ERROR_CONNECTING_TO_SERVER)
            return
        self._out_queue.publish(events.CONNECTED_TO_SERVER)

    @handler(events.LOAD_ROOMS)
    def load_rooms(self):
        response = self._connection.request(type=protocol.GET_ROOMS)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        self._out_queue.publish(events.ROOMS_LOADED, response['rooms'])

    @handler(events.JOIN_GAME)
    def join_game(self, id):
        response = self._connection.request(type=protocol.JOIN_ROOM, id=id)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        if not response["started"]:
            self._out_queue.publish(events.ROOM_JOINED, **response)

    @handler(events.CREATE_ROOM)
    def create_room(self, name, max_users):
        response = self._connection.request(type=protocol.REQUEST_CREATE_ROOM, name = name, max_users = max_users)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        logger.info('Room created')
        self._out_queue.publish(events.ROOM_CREATED, **response)

    @handler(events.CELL_EDITED)
    def cell_edited(self, square, prev_value, new_value):
        x = ord(square[0]) - ord('A')
        y = int(square[1]) - 1

        response = self._connection.request(type=protocol.SET_SUDOKU_VALUE, x=x, y=y, prev=prev_value, value=new_value)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return

    @handler(events.LEAVE_ROOM)
    def leave_room(self):
        response = self._connection.request(type=protocol.LEAVE_ROOM)
        self._out_queue.publish(events.ROOM_LEAVED)

    def __set_name_request(self):
        response = self._connection.request(type=protocol.SET_NAME, name=self._session['nickname'])
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return

    @handler(events.GAME_ENDED)
    def game_ended(self):
        pass
