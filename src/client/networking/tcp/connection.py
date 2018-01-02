from client.networking.connection import Connection
from client.networking.tcp.notifications_listener import NotificationsListener
from client.networking.tcp.blocking_connection import BlockingConnection
import logging


logger = logging.getLogger(__name__)


class TCPConnection(Connection):
    def __init__(self, out_queue):
        Connection.__init__(self, out_queue)
        self._notifications_listener = NotificationsListener(self.out_queue)
        self._connection = BlockingConnection()

    def shutdown(self):
        self._notifications_listener.shutdown()
        self._connection.shutdown()

    def connect(self, server):
        port = self._notifications_listener.bind()
        self._notifications_listener.listen_in_thread()
        self._connection.connect(server)
        return port

    def request(self, *args, **kwargs):
        return self._connection.request(*args, **kwargs)



