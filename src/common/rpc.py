from SimpleXMLRPCServer import SimpleXMLRPCServer
import socket
import logging


logger = logging.getLogger(__name__)


class CustomXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, addr, **kwargs):
        SimpleXMLRPCServer.__init__(self, addr, **kwargs)
        self.should_shutdown = False

    def serve_forever(self, poll_interval=0.5):
        self.timeout = 5
        while not self.should_shutdown:
            try:
                self.handle_request()
            except socket.error:
                continue
        logger.info('Stop serving')

    def shutdown(self):
        self.should_shutdown = True
