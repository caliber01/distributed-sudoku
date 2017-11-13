import socket
import logging
import common.networking as networking
from common.protocol import CLIENT_START_LISTEN

logger = logging.getLogger(__name__)


class RequestResponseConnection(object):
    def __init__(self):
        self.server = None
        self.s = None

    def connect(self, server, local_listening_port):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.server)
        networking.request(self.s, type=CLIENT_START_LISTEN, port=local_listening_port)

    def request(self, type, **kargs):
        return networking.request(self.s, type=type, **kargs)
