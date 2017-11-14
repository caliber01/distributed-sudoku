import client.events as events
import common.protocol as protocol
from common.listener import Listener, handler
from threading import Thread
from client.request_response import RequestResponseConnection
import logging

logger = logging.getLogger(__name__)


class ClientLogic(Listener):
    """
    Class to react on GUI events, call networking requests, notify GUI about new state
    Runs in separate thread
    """
    def __init__(self, in_queue, out_queue, listening_port):
        """
        :param in_queue: queue to subscribe to events (Subscription done in Listener baseclass)
        :param out_queue: queue to publish events for GUI
        """
        super(ClientLogic, self).__init__(in_queue)
        self._out_queue = out_queue
        self._session = {}
        self._listening_port = listening_port

        self._is_running = True
        self._thread = Thread(target=self.run)
        self._thread.start()
        self._connection = RequestResponseConnection()

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
            self._connection.connect(server, self._listening_port)
            self.__set_name_request()
        except Exception as e:
            logger.error(e)
            self._out_queue.publish(events.ERROR_CONNECTING_TO_SERVER)
            return
        self._out_queue.publish(events.CONNECTED_TO_SERVER)

    @handler(events.LOAD_ROOMS)
    def load_rooms(self):
        response = self._connection.request(type=protocol.REQUEST_ROOMS)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        self._out_queue.publish(events.ROOMS_LOADED, response['rooms'])

    @handler(events.CREATE_ROOM)
    def create_room(self, name, max_users):
        response = self._connection.request(type=protocol.REQUEST_CREATE_ROOM, name = name, max_users = max_users)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        self._out_queue.publish(events.ROOM_CREATED, **response)


    @handler(events.MESSAGE)
    def message(self, message):
        response = self._connection.request(type=protocol.PRINT_MESSAGE, message=message)
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return
        #self._out_queue.publish

    def __set_name_request(self):
        response = self._connection.request(type=protocol.SET_NAME, name=self._session['nickname'])
        if response['type'] != protocol.RESPONSE_OK:
            self._out_queue.publish(events.ERROR_OCCURRED)
            return