import socket
import logging
import common.networking as networking

logger = logging.getLogger(__name__)


class BlockingConnection(object):
    def __init__(self):
        self.s = None

    def connect(self, server):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Connecting to server at " + str(server))
        self.s.connect(server)
        logger.info("Connected")

    def request(self, type, **kwargs):
        return networking.request(self.s, type=type, **kwargs)

    def shutdown(self):
        if not self.s:
            return
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
