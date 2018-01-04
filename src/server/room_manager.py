from server.room import Room


class RoomManager(object):
    def __init__(self):
        """
        creates room manager that has list of rooms and logger
        """
        self.__rooms = []
        self.__clients = {}

    def add_client(self, client):
        self.__clients[client.id] = client

    def add_to_room(self, room_id, client_id):
        self.get_room_by_id(room_id).add_client(self.__clients[client_id])

    def create_room(self, name, max_users):
        """
        creates a new room
        """
        room = Room(name, max_users)
        self.__rooms.append(room)
        return room

    def get_available_rooms(self):
        """
        returns the list of availabele rooms
        available room means that this room is still in need of new players
        """
        return [room for room in self.__rooms if not room.full()]

    def get_room_by_id(self, id):
        """
        returns room with given id
        """
        room = None
        for r in self.__rooms:
            if r.id == id:
                room = r
                break
        return room

    def remove_room(self, room):
        """
        deletes given room from list of rooms
        """
        if room in self.__rooms:
            self.__rooms.remove(room)

    def shutdown(self):
        for client in self.__clients.values():
            client.shutdown()
