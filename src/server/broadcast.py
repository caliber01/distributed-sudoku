import common.protocol as protocol
import socket
import time
from threading import Thread
import logging


logger = logging.getLogger(__name__)


class ServerBroadcaster(Thread):
    def __init__(self, uri, shutdown_event):
        super(ServerBroadcaster, self).__init__(target=self._run)
        self.uri = uri
        self._shutdown_event = shutdown_event
        self.start()

    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        while True:
            if self._shutdown_event.is_set():
                logger.info('Shutting down server broadcasting')
                sock.close()
                break
            logger.info('Multicasting server address')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.sendto(str(self.uri).encode('utf8'), (protocol.MCAST_GRP, protocol.MCAST_PORT))
            time.sleep(5)
