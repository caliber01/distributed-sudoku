from server.room import Room

class RoomManager(object):
    def __init__(self, logger):
        self.__rooms = []
        self._logger = logger

    def create_room(self, name, max_users):
        room = Room(name, max_users, self._logger)
        self.__rooms.append(room)
        return room

    def get_rooms(self):
        return [room for room in self.__rooms if not room.full()]