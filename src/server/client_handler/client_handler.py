from common.protocol import *
from common.listener import handler
from collections import defaultdict
import uuid


class ClientHandlerBase(object):
    def __init__(self, room_manager):
        self.room_manager = room_manager
        self.room = None
        self.name = "Undefined"
        self.id = str(uuid.uuid1())
        self.handlers = defaultdict(list)
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'handled_event'):
                self.handlers[attr.handled_event].append(attr)

    def leave_room_remove(self):
        if self.room is not None:
            self.room.remove_client(self)
            if not len(self.room.users):
                self.room_manager.remove_room(self.room)
            self.room = None

    def send_notification(self, type, **kwargs):
        for handler in self.handlers[type]:
            handler(**kwargs)

    def run(self):
        raise NotImplementedError()

    def send_client_port(self, port):
        raise NotImplementedError()

    def set_sudoku_value(self, name, x, y, value, previous):
        raise NotImplementedError()

    def set_name(self, name):
        raise NotImplementedError()

    def join_to_room(self, id):
        raise NotImplementedError()

    def create_room(self, name, max_users):
        raise NotImplementedError()

    def get_available_rooms(self):
        raise NotImplementedError()

    def __leave_room(self):
        raise NotImplementedError()

    def __start_game(self, **kwargs):
        raise NotImplementedError()

    def __people_changed(self, **kwargs):
        raise NotImplementedError()

    def __sudoku_solved(self, **kwargs):
       raise NotImplementedError()

    def __sudoku_changed(self, **kwargs):
        raise NotImplementedError()
