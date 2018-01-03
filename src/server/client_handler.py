from common.protocol import *
from common.listener import Listener, handler
from collections import defaultdict
import uuid


class ClientHandler(Listener):
    def __init__(self, connection, room_manager):
        super(ClientHandler, self).__init__()
        self.id = str(uuid.uuid1())
        self.connection = connection
        self.handlers = defaultdict(list)
        self.room_manager = room_manager
        self.room = None
        self.name = "Undefined"

    def run(self):
        self.connection.listen(on_message=lambda type, *args, **kwargs: self.handle_event(type, kwargs),
                               on_terminate=self.leave_room_remove)

    def leave_room_remove(self):
        if self.room != None:
            self.room.remove_client(self)
            if not len(self.room.users):
                self.room_manager.remove_room(self.room)
            self.room = None

    @handler(PRINT_MESSAGE)
    def print_message(self, args):
        print(args['message'])
        self.connection.respond(RESPONSE_OK)

    @handler(CLIENT_START_LISTEN)
    def send_client_port(self, args):
        self.connection.open_notifications_connection(args)
        self.connection.respond(RESPONSE_OK)

    @handler(SET_SUDOKU_VALUE)
    def set_sudoku_value(self, args):
        if self.room.set_value(name=self.id, **args):
            self.connection.respond(RESPONSE_OK)
        else:
            self.connection.respond(TOO_LATE)

    @handler(GET_SCORE)
    def get_score(self):
        self.room.get_score()

    @handler(SET_NAME)
    def set_name(self, args):
        self.name = args["name"]
        self.connection.respond(RESPONSE_OK)

    @handler(JOIN_ROOM)
    def join_to_room(self, args):
        self.room = self.room_manager.get_room_by_id(args["id"])
        if self.room != None:
            try:
                self.room.add_client(self)
                if self.room.game_started:
                    self.connection.respond(RESPONSE_OK, started=True, name=self.room.name)
                else:
                    names = []
                    for user in self.room.users:
                        names.append(user.name)
                    self.connection.respond(RESPONSE_OK, started=False, users=names, name=self.room.name, max=self.room.max_users, need_users=(self.room.max_users - len(names)))
            except:
                self.connection.notify(TOO_LATE)
        else:
            self.connection.respond(NOT_FOUND)

    @handler(REQUEST_CREATE_ROOM)
    def create_room(self, args):
        room = self.room_manager.create_room(args["name"], args["max_users"])
        self.connection.respond(RESPONSE_OK, name=room.name, max=room.max_users)
        room.add_client(self)
        self.room = room
        print("room created %s %d" % (room.name, room.max_users))

    def send_notification(self, type, **kwargs):
        self.handle_event(type, **kwargs)

    @handler(GET_ROOMS)
    def get_available_rooms(self, args):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        self.connection.respond(RESPONSE_OK, rooms = rooms)

    @handler(LEAVE_ROOM)
    def __leave_room(self, args):
       self.leave_room_remove()
       self.connection.respond(RESPONSE_OK)

    @handler(START_GAME)
    def __start_game(self, **kwargs):
        response = self.connection.notify(**kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(PEOPLE_CHANGED)
    def __people_changed(self, **kwargs):
        response = self.connection.notify(type=PEOPLE_CHANGED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(SUDOKU_SOLVED)
    def __sudoku_solved(self, **kwargs):
        response = self.connection.notify(type=SUDOKU_SOLVED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    @handler(SUDOKU_CHANGED)
    def __sudoku_changed(self, **kwargs):
        response = self.connection.notify(type=SUDOKU_CHANGED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return
