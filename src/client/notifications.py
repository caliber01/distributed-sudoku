import socket
from Queue import Empty
import common.protocol as protocol
import common.networking as networking
from threading import Thread
import client.events as events
import logging
import errno

logger = logging.getLogger(__name__)


class NotificationsConnection():
    """
    Object that binds a socket to accept connection from server
    and listen to notifications
    """
    def __init__(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 0))
        self.port = self.s.getsockname()[1]
        self.notifications_socket = None
        self._t = Thread(target=self._run)
        self._t.start()

    def _should_shutdown(self):
        try:
            event = self.in_queue.get_nowait()[0]
            return event is events.QUIT
        except Empty:
            return False

    def _shutdown(self):
        logger.info('Shutting down notifications listener')
        if not self.notifications_socket:
            return
        self.notifications_socket.shutdown(socket.SHUT_RDWR)
        self.notifications_socket.close()

    def _run(self):
        self.s.listen(1)
        self.s.settimeout(1)
        while True:
            if self._should_shutdown():
                self._shutdown()
                return
            try:
                self.notifications_socket, address = self.s.accept()
                break
            except socket.timeout:
                continue

        self.s.close()
        self.notifications_socket.settimeout(1)

        while True:
            if self._should_shutdown():
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



