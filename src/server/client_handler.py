from common.networking import recv, send
from common.protocol import *
from common.listener import handler
import socket
from collections import defaultdict
from common.networking import request
import uuid

class ClientHandler(object):
    def __init__(self, s, room_manager, logger):
        self.id = str(uuid.uuid1())
        self._logger = logger
        self.socket = s
        self.s_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handlers = defaultdict(list)
        self.room_manager = room_manager
        self.room = None
        self.name = "Undefined"
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'handled_event'):
                self.handlers[attr.handled_event].append(attr)

    def run(self):
        while True:
            try:
                message = recv(self.socket)
                type = message['type']
                for handler in self.handlers[type]:
                    handler(message)
            except:
                self._logger.debug("Exception occurs in client %s" % (self.name))


    @handler(PRINT_MESSAGE)
    def print_message(self, args):
        print(args['message'])
        self.__send(RESPONSE_OK)


    @handler(CLIENT_START_LISTEN)
    def send_client_port(self, args):
        self.s_to_client.connect((self.socket.getpeername()[0], args["port"]))
        self.__send(RESPONSE_OK)

    @handler(SET_SUDOKU_VALUE)
    def set_sudoku_value(self, args):
        if self.room.set_value(args["x"], args["y"], args["value"], args["prev"]):
            self.__send(RESPONSE_OK)
        else:
            self.__send(TOO_LATE)

    @handler(GET_SCORE)
    def get_score(self):
        self.room.get_score()

    @handler(SET_NAME)
    def set_name(self, args):
        self.name = args["name"]
        self.__send(RESPONSE_OK)

    @handler(JOIN_ROOM)
    def join_to_room(self, args):
        room = self.room_manager.get_room_by_id(args["id"])
        if room != None:
            room.add_client(self)
            self.__send(RESPONSE_OK, name=room.name, max = room.max_users, current = len(room.users), users=[user.name for user in room.users])
        else:
            self.__send(NOT_FOUND)

    @handler(REQUEST_CREATE_ROOM)
    def create_room(self, args):
        room = self.room_manager.create_room(args["name"], args["max_users"])
        room.add_client(self)
        self.room = room
        self.__send(RESPONSE_OK, name=room.name, max=room.max_users, current=len(room.users), users=[user.name for user in room.users])
        print("room creted %s %d" % (room.name, room.max_users))

    def send_notification(self, type, **args):
        for handler in self.handlers[type]:
            handler(args)

    @handler(GET_ROOMS)
    def get_available_rooms(self):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        self.__send(RESPONSE_OK, rooms = rooms)

    def __request(self, type, **kargs):
        return request(self.s, type=type, **kargs)

    @handler(START_GAME)
    def __start_game(self, **kargs):
        response = request(self.s, type=START_GAME, **kargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    def __send(self, type, **kargs):
        try:
            send(self.socket, type=type, **kargs)
        except:
            self.logger.debug("Exception occurs in client %s" % (self.name))
