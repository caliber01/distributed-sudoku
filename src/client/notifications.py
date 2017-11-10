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
        self.notifications_socket = None
        self._t = Thread(target=self.run)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', protocol.DEFAULT_CLIENT_LISTENER_PORT))
        s.listen(1)
        self.notifications_socket = s.accept()
        s.close()
        while True:
            notification = networking.recv(socket)
            self.out_queue.publish(notification['type'], **notification)



