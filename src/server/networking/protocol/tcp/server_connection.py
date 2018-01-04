import socket
import logging
from server.networking.protocol.tcp.client_connection import TCPClientConnection
from server.networking.protocol.client_proxy import ProtocolClientProxy
from server.networking.server_connection import ServerConnection
from server.client_handler import ClientHandler


logger = logging.getLogger(__name__)


class TCPServerConnection(ServerConnection):
    def __init__(self, ip, port, room_manager):
        self.room_manager = room_manager
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def accept_connections(self, shutdown_event):
        logger.debug('Server socket created, descriptor %d' % self.s.fileno())
        self.s.bind((self.ip, self.port))
        logger.debug('Server socket bound on %s:%d' % self.s.getsockname())
        logger.info('Accepting requests on TCP %s:%d' % self.s.getsockname())
        self.s.listen(10000)
        self.s.settimeout(5)
        while True:
            if shutdown_event.is_set():
                break
            try:
                logger.debug('Awaiting requests ...')
                client_socket, endpoint = self.s.accept()
                logger.debug('Created client handler for  %s:%d' % client_socket.getsockname())
                connection = TCPClientConnection(client_socket)
                client_handler = ClientHandler(self.room_manager)
                client = ProtocolClientProxy(client_handler, connection)
                self.room_manager.add_client(client)
            except socket.timeout:
                continue
            except:
                logger.exception('Exception occurs in main thread')
                break
        self.s.close()
