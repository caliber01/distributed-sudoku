import socket
import logging
import common.networking as networking

logger = logging.getLogger(__name__)

class Networking(object):
    def __init__(self):
        self.server = None
        self.s = None

    def connect(self, server):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.server)

    def request(self, *args, **kargs):
        return networking.request(self.s, *args, **kargs)


