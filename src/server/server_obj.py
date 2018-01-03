from threading import Thread
from server.client_handler import ClientHandler
from server.room_manager import RoomManager


class Server(object):
    def __init__(self, server_connection):
        self.server_connection = server_connection
        self.clients = {}
        self.room_manager = RoomManager()

    def new_client(self, connection):
        client = ClientHandler(connection, self.room_manager)
        self.clients[client.id] = client
        t = Thread(target=client.run)
        t.start()

    def run(self):
        self.server_connection.accept_connections(on_connection=self.new_client)


