from common.protocol import *
from common.listener import Listener, handler
from threading import Thread
from server.networking.client_proxy import ClientProxy


class ProtocolClientProxy(ClientProxy, Listener):
    def __init__(self, client, connection):
        self.client = client
        super(ProtocolClientProxy, self).__init__()
        self.connection = connection
        self._t = Thread(target=self._run)
        self._t.start()

    @property
    def room(self):
        return self.client.room

    @property
    def id(self):
        return self.client.id

    @property
    def name(self):
        return self.client.name

    def _run(self):
        self.connection.listen(on_message=self.handle_event,
                               on_terminate=self.client.leave_room_remove)

    @handler(CLIENT_START_LISTEN)
    def __send_client_port(self, **kwargs):
        return self.connection.open_notifications_connection(**kwargs)

    @handler(SET_SUDOKU_VALUE)
    def __set_sudoku_value(self, **kwargs):
        return self.client.set_sudoku_value(**kwargs)

    @handler(SET_NAME)
    def __set_name(self, **kwargs):
        return self.client.set_name(**kwargs)

    @handler(JOIN_ROOM)
    def __join_to_room(self, **kwargs):
        return self.client.join_to_room(**kwargs)

    @handler(REQUEST_CREATE_ROOM)
    def __create_room(self, **kwargs):
        return self.client.create_room(**kwargs)

    @handler(GET_ROOMS)
    def __get_available_rooms(self, **kwargs):
        return self.client.get_available_rooms(**kwargs)

    @handler(LEAVE_ROOM)
    def __leave_room(self, **kwargs):
        return self.client.leave_room(**kwargs)

    def notify_start_game(self, **kwargs):
        response = self.connection.notify(type=START_GAME, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    def notify_people_changed(self, **kwargs):
        response = self.connection.notify(type=PEOPLE_CHANGED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    def notify_sudoku_solved(self, **kwargs):
        response = self.connection.notify(type=SUDOKU_SOLVED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return

    def notify_sudoku_changed(self, **kwargs):
        response = self.connection.notify(type=SUDOKU_CHANGED, **kwargs)
        # TODO Process error
        if response['type'] != RESPONSE_OK:
            return