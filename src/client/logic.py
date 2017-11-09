import client.events as events
import common.protocol as protocol
import types
from common.listener import Listener, handler
from threading import Thread
from client.networking import Networking
import logging

logger = logging.getLogger(__name__)


class ClientLogic(Listener):
    """
    Class to react on GUI events, call networking requests, notify GUI about new state
    Runs in separate thread
    """
    def __init__(self, in_queue, out_queue):
        """
        :param in_queue: queue to subscribe to events (Subscription done in Listener baseclass)
        :param out_queue: queue to publish events for GUI
        """
        super().__init__(in_queue)
        self._out_queue = out_queue
        self._session = {}

        self._thread = Thread(target=self.run)
        self._thread.start()
        self._networking = None

    @handler(events.SUBMIT_NICKNAME)
    def submit_nickname(self, nickname):
        self._session['nickname'] = nickname
        logger.info(nickname)

    @handler(events.CONNECT_TO_SERVER)
    def connect_to_server(self, server):
        self._session['server'] = server
        self._networking = Networking(server)
        try:
            self._networking.connect()
        except Exception as e:
            logger.error(e)
            self._out_queue.put(events.ERROR_CONNECTING_TO_SERVER)


