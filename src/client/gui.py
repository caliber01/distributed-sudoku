import Tkinter
import client.events as events
from common.listener import Listener, handler


class UI(Listener):
    """
    Main class for user interface, runs in the main thread
    """

    def __init__(self, in_queue, out_channel):
        """
        :param in_queue: incoming messages queue
        :param out_channel: messages queue to publish events for ClientLogic
        """
        super(UI, self).__init__(in_queue)
        self.out_channel = out_channel

    def render_welcome(self):
        self.out_channel.publish(events.SUBMIT_NICKNAME, "Mynickname")


