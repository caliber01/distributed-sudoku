from client.networking.host import Host
import common.protocol as protocol
from common.errors import error_by_code


class ManualHost(Host):
    def __init__(self, connection):
        self._connection = connection

    def connect(self, server):
        self._connection.connect(server)

    def set_name(self, name):
        return self._request(type=protocol.SET_NAME, name=name)

    def load_rooms(self):
        response = self._request(type=protocol.GET_ROOMS)
        return response['rooms']

    def join_game(self, id):
        response = self._request(type=protocol.JOIN_ROOM, id=id)
        return response

    def create_room(self, name, max_users):
        return self._request(type=protocol.REQUEST_CREATE_ROOM, name = name, max_users = max_users)

    def cell_edited(self, x, y, prev_value, new_value):
        return self._request(type=protocol.SET_SUDOKU_VALUE, x=x, y=y, previous=prev_value, value=new_value)

    def leave_room(self):
        return self._request(type=protocol.LEAVE_ROOM)

    def _request(self, **kwargs):
        response = self._connection.request(**kwargs)
        if response['type'] != protocol.RESPONSE_OK:
            raise error_by_code(response['type'])
        return response

    def shutdown(self):
        self._connection.shutdown()
