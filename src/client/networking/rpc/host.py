from client.networking.host import Host
from client.networking.rpc.player import Player
from xmlrpclib import ServerProxy
import common.protocol as protocol
import socket


class RPCHost(Host):
    def __init__(self, gui_queue):
        self.host = None
        self.player = None
        self.listen_thread = None
        self.server_port = None
        self.gui_queue = gui_queue

    def connect(self, server):
        self.host = ServerProxy("http://%s:%d" % server)
        self.server_port = self.host.connect(socket.gethostbyname(socket.gethostname()))
        self.host = ServerProxy("http://%s:%d" % (server[0], self.server_port), allow_none=True)
        self.player = Player(self.gui_queue)
        self.player.start()
        self.host.open_notifications_connection(self.player.get_address())

    def set_name(self, name):
        self.host.set_name(name)

    def load_rooms(self):
        return self.host.get_available_rooms()['rooms']

    def join_game(self, id):
        return self.host.join_to_room(id)

    def create_room(self, name, max_users):
        return self.host.create_room(name, max_users)

    def cell_edited(self, x, y, prev_value, new_value):
        return self.host.set_sudoku_value(x, y, new_value, prev_value)

    def leave_room(self):
        return self.host.leave_room()

    def shutdown(self):
        self.host.terminate()
