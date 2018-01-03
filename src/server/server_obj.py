from threading import Thread
from server.client_handler.tcp_indirect.client_handler import TCPClientHandler
from server.client_handler.rpc.client_handler import RPCClientHandler
from server.room_manager import RoomManager
from server.server_types import *


class Server(object):
    def __init__(self, server_connection, client_handler_type):
        self.server_connection = server_connection
        self.client_handler_type = client_handler_type
        self.clients = {}
        self.room_manager = RoomManager()

    def new_client(self, connection):
        if self.client_handler_type == TCP:
            client = TCPClientHandler(connection, self.room_manager)
        elif self.client_handler_type == RPC:
            client = RPCClientHandler(connection, self.room_manager)
        else:
            pass
        self.clients[client.id] = client
        t = Thread(target=client.run)
        t.start()

    def run(self):
        self.server_connection.accept_connections(on_connection=self.new_client)


