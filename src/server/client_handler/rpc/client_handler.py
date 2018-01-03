import threading
from common.protocol import *
from common.listener import handler
from server.client_handler.client_handler import ClientHandlerBase


# TODO stop

class RPCClientHandler(ClientHandlerBase):
    def __init__(self, connection, room_manager):
        super(RPCClientHandler, self).__init__(room_manager)
        self.connection = connection
        self.connection.register_functions(self)
        self.listen_thread = None

    def run(self):
        self.listen_thread = threading.Thread(target=self.connection.listen)
        self.listen_thread.start()

    def __handle_event(self, t, message):
        for h in self.handlers[t]:
            h(message)

    def send_client_port(self, port):
        self.connection.open_notifications_connection(port)
        return True

    @handler(SET_SUDOKU_VALUE)
    def __set_sudoku_value(self, args):
        self.set_sudoku_value(args["x"], args["y"], args["value"], args["previous"])

    def set_sudoku_value(self, x, y, value, previous):
        if self.room.set_value(self.id, x, y, value, previous):
            return RESPONSE_OK
        else:
            return TOO_LATE

    def set_name(self, name):
        self.name = name
        return True

    def join_to_room(self, id):
        self.room = self.room_manager.get_room_by_id(id)
        if self.room != None:
            try:
                self.room.add_client(self)
                if self.room.game_started:
                    return RESPONSE_OK, {"started": True, "name": self.room.name}
                else:
                    names = []
                    for user in self.room.users:
                        names.append(user.name)
                    return RESPONSE_OK, {"started": False, "users": names, "name": self.room.name,
                                         "max": self.room.max_users, "need_users": (self.room.max_users - len(names))}
            except:
                return TOO_LATE
        else:
            return NOT_FOUND

    def create_room(self, name, max_users):
        room = self.room_manager.create_room(name, max_users)
        room.add_client(self)
        self.room = room
        print("room created %s %d" % (room.name, room.max_users))
        return RESPONSE_OK, {"name": room.name, "max": room.max_users}

    def get_available_rooms(self):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        return rooms

    def leave_room(self):
        self.leave_room_remove()
        return RESPONSE_OK

    def terminate(self):
        self.connection.terminate()

    @handler(START_GAME)
    def __start_game(self, **kwargs):
        self.connection.proxy.start_game(kwargs)

    @handler(PEOPLE_CHANGED)
    def __people_changed(self, **kwargs):
        self.connection.proxy.people_changed(kwargs)

    @handler(SUDOKU_SOLVED)
    def __sudoku_solved(self, **kwargs):
        self.connection.proxy.sudoku_solved(kwargs)

    @handler(SUDOKU_CHANGED)
    def __sudoku_changed(self, **kwargs):
        self.connection.proxy.sudoku_changed(kwargs)