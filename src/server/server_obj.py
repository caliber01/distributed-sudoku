class Server(object):
    def __init__(self, server_connection, room_manager):
        self.room_manager = room_manager
        self.server_connection = server_connection

    def run(self):
        self.server_connection.accept_connections(
            on_connection=self.room_manager.add_client)


