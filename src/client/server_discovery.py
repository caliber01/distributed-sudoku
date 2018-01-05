from threading import Thread, Event
import socket
import common.protocol as protocol
import struct
import logging
import client.events as events
import time


logger = logging.getLogger(__name__)


class ServerDiscovery(Thread):
    def __init__(self, gui_queue):
        self.gui_queue = gui_queue
        self._shutdown_event = None
        super(ServerDiscovery, self).__init__(target=self._run)

    def start(self):
        logger.info('Start server discovery')
        self._servers = {}
        self._shutdown_event = Event()
        super(ServerDiscovery, self).start()

    def prune_servers(self):
        self._servers = {server:timestamp for server, timestamp in self._servers.items()
                         if time.time() - timestamp < 30}

    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', protocol.MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(protocol.MCAST_GRP), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        sock.settimeout(5)
        while True:
            self.prune_servers()
            self.gui_queue.publish(events.DISCOVERED_SERVERS, servers=self._servers.keys())
            if self._shutdown_event.is_set():
                sock.close()
                break
            try:
                uri = sock.recv(1024).decode('utf8')
                self._servers[uri] = time.time()
                logger.info('Received server URI: {}'.format(uri))
            except socket.timeout:
                continue

    def shutdown(self):
        if self._shutdown_event:
            self._shutdown_event.set()
            logger.info('Stop server discovery')
