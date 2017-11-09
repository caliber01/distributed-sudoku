import socket
import logging

logger = logging.getLogger(__name__)


class Networking(object):
    def __init__(self, server):
        self.server = server

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.server)


