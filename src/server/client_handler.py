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
        try:
            while True:
                message = recv(self.socket)
                if not message:
                    self.leave_room_remove()
                    break
                self._logger.info("New request from client %s" % (self.name))
                self._logger.info(message)
                type = message['type']
                for handler in self.handlers[type]:
                    handler(message)
        except:
            self._logger.exception("Exception occurs in client %s" % (self.name))
            self.leave_room_remove()

    def leave_room_remove(self):
        if self.room != None:
            self.room.remove_client(self)
            if not len(self.room.users):
                self.room_manager.remove_room(self.room)
            self.room = None

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
        if self.room.set_value(name=self.id, **args):
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
        self.room = self.room_manager.get_room_by_id(args["id"])
        if self.room != None:
            try:
                self.room.add_client(self)
                if self.room.game_started:
                    self.__send(RESPONSE_OK, started=True, name=self.room.name)
                else:
                    names = []
                    for user in self.room.users:
                        names.append(user.name)
                    self.__send(RESPONSE_OK, started=False, users=names, name=self.room.name, max=self.room.max_users, need_users=(self.room.max_users - len(names)))
            except:
                self.__send(TOO_LATE)
        else:
            self.__send(NOT_FOUND)

    @handler(REQUEST_CREATE_ROOM)
    def create_room(self, args):
        room = self.room_manager.create_room(args["name"], args["max_users"])
        self.__send(RESPONSE_OK, name=room.name, max=room.max_users)
        room.add_client(self)
        self.room = room
        print("room creted %s %d" % (room.name, room.max_users))

    def send_notification(self, type, **args):
        for handler in self.handlers[type]:
            handler(**args)

    @handler(GET_ROOMS)
    def get_available_rooms(self, args):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        self.__send(RESPONSE_OK, rooms = rooms)

    @handler(LEAVE_ROOM)
    def __leave_room(self, args):
       self.leave_room_remove()
       self.__send(RESPONSE_OK)

    @handler(START_GAME)
    def __start_game(self, **kargs):
        response = request(self.s_to_client, type=START_GAME, **kargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(PEOPLE_CHANGED)
    def __people_changed(self, **kargs):
        response = request(self.s_to_client, type=PEOPLE_CHANGED, **kargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(SUDOKU_SOLVED)
    def __sudoku_solved(self, **kargs):
        response = request(self.s_to_client, type=SUDOKU_SOLVED, **kargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(SUDOKU_CHANGED)
    def __sudoku_changed(self, **kargs):
        response = request(self.s_to_client, type=SUDOKU_CHANGED, **kargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    def __send(self, type, **kargs):
        try:
            send(self.socket, type=type, **kargs)
        except:
            self._logger.debug("Exception occurs in client %s" % (self.name))
