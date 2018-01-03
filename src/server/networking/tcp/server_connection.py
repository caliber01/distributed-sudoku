import socket
import logging
from server.networking.tcp.client_connection import TCPClientConnection
from server.networking.server_connection import ServerConnection


logger = logging.getLogger(__name__)


class TCPServerConnection(ServerConnection):
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def accept_connections(self, on_connection):
        logger.debug('Server socket created, descriptor %d' % self.s.fileno())
        self.s.bind((self.ip, self.port))
        logger.debug('Server socket bound on %s:%d' % self.s.getsockname())
        logger.info('Accepting requests on TCP %s:%d' % self.s.getsockname())
        self.s.listen(10000)
        while True:
            try:
                logger.debug('Awaiting requests ...')
                client_socket, endpoint = self.s.accept()
                logger.debug('Created client handler for  %s:%d' % client_socket.getsockname())
                connection = TCPClientConnection(client_socket)
                on_connection(connection)
            except:
                logger.info('Exception occurs in main thread')
                break
        self.s.close()
