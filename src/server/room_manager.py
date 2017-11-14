from server.room import Room

class RoomManager(object):
    def __init__(self):
        self.rooms = []

    def create_room(self, name, max_users):
        room = Room(name, max_users)
        self.rooms.append(room)
        return room