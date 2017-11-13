import socket
import common.protocol as protocol
import common.networking as networking
from threading import Thread


class NotificationsConnection():
    """
    Object that binds a socket to accept connection from server
    The socket with server is receive-only
    """
    def __init__(self, out_queue):
        self.out_queue = out_queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 0))
        self.port = self.s.getsockname()[1]
        self.notifications_socket = None
        self._t = Thread(target=self.run)
        self._t.start()

    def run(self):
        self.s.listen(1)
        self.notifications_socket, endpoint = self.s.accept()
        self.s.close()
        while True:
            notification = networking.recv(self.notifications_socket)
            self.out_queue.publish(notification['type'], **notification)



