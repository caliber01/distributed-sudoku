from common.networking import recv, send, request
from server.networking.client_connection import ClientConnection
import logging
import socket

logger = logging.getLogger(__name__)


class TCPClientConnection(ClientConnection):
    def __init__(self, client_socket):
        super(TCPClientConnection, self).__init__()
        self.socket = client_socket
        self.s_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, on_message, on_terminate):
        try:
            while True:
                message = recv(self.socket)
                if not message:
                    on_terminate()
                    break
                logger.info("New request from client %s" % (self.name))
                logger.info(message)
                type = message['type']
                on_message(type, message)
        except:
            logger.exception("Exception occurs in client %s" % (self.name))
            on_terminate()

    def respond(self, type, **kwargs):
        try:
            send(self.socket, type=type, **kwargs)
        except:
            logger.debug("Exception occurs in client %s" % (self.name))

    def open_notifications_connection(self, args):
        self.s_to_client.connect((self.socket.getpeername()[0], args["port"]))

    def notify(self, type, **kwargs):
        return request(self.s_to_client, type=type, **kwargs)