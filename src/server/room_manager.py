from server.room import Room

class RoomManager(object):
    def __init__(self, logger):
        self.__rooms = []
        self._logger = logger

    def create_room(self, name, max_users):
        room = Room(name, max_users, self._logger)
        self.__rooms.append(room)
        return room

    def get_available_rooms(self):
        return [room for room in self.__rooms if not room.full()]

    def get_room_by_id(self, id):
        room = None
        for r in self.__rooms:
            if r.id == id:
                room = r
                break
        return room

    def remove_room(self, room):
        if room in self.__rooms:
            self.__rooms.remove(room)