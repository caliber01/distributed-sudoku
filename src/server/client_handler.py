from common.errors import *
import uuid


class ClientHandler(object):
    def __init__(self, room_manager):
        self.id = str(uuid.uuid1())
        self.room_manager = room_manager
        self.room = None
        self.name = "Undefined"

    def leave_room_remove(self):
        if self.room is not None:
            self.room.remove_client(self.id)
            if not len(self.room.users):
                self.room_manager.remove_room(self.room)
            self.room = None

    def set_sudoku_value(self, x, y, value, previous):
        self.room.set_value(self.id, x, y, value, previous)

    def set_name(self, name):
        self.name = name

    def join_to_room(self, id):
        self.room = self.room_manager.get_room_by_id(id)
        self.room_manager.add_to_room(id, self.id)
        if self.room is not None:
            if self.room.game_started:
                return {"started": True, "name": self.room.name}
            else:
                names = [user.name for user in self.room.users]
                return {"started": False, "users": names,
                        "name": self.room.name,
                        "max": self.room.max_users,
                        "need_users": (self.room.max_users - len(names))}
        else:
            raise RoomNotFoundError()

    def create_room(self, name, max_users):
        room = self.room_manager.create_room(name, max_users)
        self.room_manager.add_to_room(room.id, self.id)
        self.room = room
        return {"name": room.name, "max": room.max_users}

    def get_available_rooms(self):
        rooms = []
        for room in self.room_manager.get_available_rooms():
            rooms.append({"name": room.name, "max": room.max_users, "current": len(room.users), "id": room.id})
        return {'rooms': rooms}

    def leave_room(self):
        self.leave_room_remove()

