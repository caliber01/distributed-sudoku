import client.events as events
import common.protocol as protocol
import types
from common.listener import Listener, handler
from threading import Thread


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
        self.out_queue = out_queue
        self.session = {}

        self.thread = Thread(target=self.run)
        self.thread.start()

    @handler(events.SUBMIT_NICKNAME)
    def submit_nickname(self, nickname):
        self.session['nickname'] = nickname
        print(nickname)

    @handler(events.CONNECT_TO_SERVER)
    def connect_to_server(self, address, port):
        self.session['server'] = (address, port)



