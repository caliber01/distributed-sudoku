from common.networking import recv, send
from common.protocol import *
from common.listener import handler
import socket
from collections import defaultdict
import common.networking
import uuid

class ClientHandler(object):
    def __init__(self, s, room_manager):
        self.id = id = str(uuid.uuid1())
        self.socket = s
        self.s_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handlers = defaultdict(list)
        self.room_manager = room_manager
        self.room = None
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'handled_event'):
                self.handlers[attr.handled_event].append(attr)

    def run(self):
        while True:
            message = recv(self.socket)
            type = message['type']
            for handler in self.handlers[type]:
                handler(message)

    @handler(PRINT_MESSAGE)
    def print_message(self, args):
        print(args['message'])
        send(self.socket, type=RESPONSE_OK)


    @handler(CLIENT_START_LISTEN)
    def send_client_port(self, args):
        self.s_to_client.connect((self.socket.getpeername()[0], args["port"]))
        send(self.socket, type=RESPONSE_OK)

    @handler(REQUEST_CREATE_ROOM)
    def create_room(self, args):
        room = self.room_manager.create_room(args["name"], args["max_users"])
        room.add_client(self)
        self.room = room
        send(self.socket, type=RESPONSE_OK)
        print("room creted %s %d" % (room.name, room.max_users))

    def get_available_rooms(self):
        # TODO
        return

    def __request(self, type, **kargs):
        return common.networking.request(self.s, type=type, **kargs)