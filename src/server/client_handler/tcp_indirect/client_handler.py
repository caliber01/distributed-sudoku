from common.protocol import *
from common.listener import handler
from server.client_handler.client_handler import ClientHandlerBase


class TCPClientHandler(ClientHandlerBase):
    def __init__(self, connection, room_manager):
        super(TCPClientHandler, self).__init__(room_manager)
        self.connection = connection

    def run(self):
        self.connection.listen(on_message=lambda type, args: self.__handle_event(type, args),
                               on_terminate=self.leave_room_remove)

    def __handle_event(self, t, message):
        for h in self.handlers[t]:
            h(message)

    @handler(CLIENT_START_LISTEN)
    def __send_client_port(self, args):
        self.send_client_port(args["port"])

    def send_client_port(self, port):
        self.connection.open_notifications_connection(port)
        self.connection.respond(RESPONSE_OK)

    @handler(SET_SUDOKU_VALUE)
    def __set_sudoku_value(self, args):
        self.set_sudoku_value(args["x"], args["y"], args["value"], args["previous"])

    def set_sudoku_value(self, x, y, value, previous):
        if self.room.set_value(self.id, x, y, value, previous):
            self.connection.respond(RESPONSE_OK)
        else:
            self.connection.respond(TOO_LATE)

    @handler(SET_NAME)
    def __set_name(self, args):
        self.set_name(args["name"])

    def set_name(self, name):
        self.name = name
        self.connection.respond(RESPONSE_OK)

    @handler(JOIN_ROOM)
    def __join_to_room(self, args):
        self.join_to_room(args["id"])

    def join_to_room(self, id):
        self.room = self.room_manager.get_room_by_id(id)
        if self.room != None:
            try:
                self.room.add_client(self)
                if self.room.game_started:
                    self.connection.respond(RESPONSE_OK, started=True, name=self.room.name)
                else:
                    names = []
                    for user in self.room.users:
                        names.append(user.name)
                    self.connection.respond(RESPONSE_OK, started=False, users=names, name=self.room.name,
                                            max=self.room.max_users, need_users=(self.room.max_users - len(names)))
            except:
                self.connection.notify(TOO_LATE)
        else:
            self.connection.respond(NOT_FOUND)

    @handler(REQUEST_CREATE_ROOM)
    def __create_room(self, args):
        self.create_room(args["name"], args["max_users"])

    def create_room(self, name, max_users):
        room = self.room_manager.create_room(name, max_users)
        self.connection.respond(RESPONSE_OK, name=room.name, max=room.max_users)
        room.add_client(self)
        self.room = room
        print("room created %s %d" % (room.name, room.max_users))

    @handler(GET_ROOMS)
    def __get_available_rooms(self, args):
        self.get_available_rooms()

    def get_available_rooms(self):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        self.connection.respond(RESPONSE_OK, rooms=rooms)

    @handler(LEAVE_ROOM)
    def __leave_room(self, args):
        self.leave_room_remove()
        self.connection.respond(RESPONSE_OK)

    @handler(START_GAME)
    def __start_game(self, **kwargs):
        response = self.connection.notify(type=START_GAME, **kwargs)
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