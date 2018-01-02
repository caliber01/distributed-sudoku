import socket
import common.protocol as protocol
import common.networking as networking
from threading import Thread, Event
import logging

logger = logging.getLogger(__name__)


class NotificationsListener():
    """
    Object that binds a socket to accept connection from server
    and listen to notifications
    """
    def __init__(self, out_queue):
        self.shutdown_event = Event()
        self.out_queue = out_queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def shutdown(self):
        self.shutdown_event.set()

    def bind(self):
        self.s.bind(('', 0))
        self.notifications_socket = None
        return self.s.getsockname()[1]

    def listen_in_thread(self):
        self._t = Thread(target=self._listen)
        self._t.start()

    def _shutdown(self):
        logger.info('Shutting down notifications listener')
        if not self.notifications_socket:
            return
        self.notifications_socket.shutdown(socket.SHUT_RDWR)
        self.notifications_socket.close()

    def _listen(self):
        self.s.listen(1)
        self.s.settimeout(5)
        while True:
            if self.shutdown_event.is_set():
                self._shutdown()
                return
            try:
                self.notifications_socket, address = self.s.accept()
                break
            except socket.timeout:
                continue

        self.s.close()
        self.notifications_socket.settimeout(5)

        while True:
            if self.shutdown_event.is_set():
                self._shutdown()
                break
            try:
                notification = networking.recv(self.notifications_socket)
                logger.info('New notification')
                logger.info(notification)
                self.out_queue.publish(notification['type'], **notification)
                networking.send(self.notifications_socket, type=protocol.RESPONSE_OK)
            except socket.timeout:
                continue



