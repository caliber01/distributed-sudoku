import Tkinter
import client.events as events
from common.listener import Listener, handler


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

    def render_welcome(self):
        self.out_queue.publish(events.SUBMIT_NICKNAME, "Mynickname")
        self.out_queue.publish(events.MESSAGE, "MESSAGE")
        self.out_queue.publish(events.MESSAGE, "MESSAGE")
        self.out_queue.publish(events.MESSAGE, "MESSAGE")
        self.out_queue.publish(events.MESSAGE, "MESSAGE")

    @handler(events.ERROR_CONNECTING_TO_SERVER)
    def error_connecting_to_server(self, e):
        print(e)

