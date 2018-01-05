import threading
from common.rpc import CustomXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from xmlrpclib import ServerProxy
import logging
from server.networking.client_proxy import ClientProxy

logger = logging.getLogger(__name__)


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Host():
    def __init__(self, client_ip, client_proxy, client):
        self.client_ip = client_ip
        self.client_proxy = client_proxy
        self.client = client

    def open_notifications_connection(self, port):
        player = ServerProxy("http://%s:%d" % (self.client_ip, port))
        self.client_proxy.set_player(player)

    def leave_room_remove(self, *args):
        return self.client.leave_room_remove(*args)

    def set_sudoku_value(self, *args):
        return self.client.set_sudoku_value(*args)

    def set_name(self, *args):
        return self.client.set_name(*args)

    def join_to_room(self, *args):
        return self.client.join_to_room(*args)

    def create_room(self, *args):
        return self.client.create_room(*args)

    def get_available_rooms(self, *args):
        return self.client.get_available_rooms(*args)

    def leave_room(self, *args):
        return self.client.leave_room(*args)

    def terminate(self):
        self.client_proxy.player.terminate()
        self.client.leave_room_remove()


# TODO stop
class RPCClientProxy(ClientProxy):
    def __init__(self, client, client_ip):
        super(RPCClientProxy, self).__init__()
        self.client = client
        self.client_ip = client_ip
        self.player = None
        self.server = CustomXMLRPCServer(('0.0.0.0', 0), allow_none=True)
        self.server.register_introspection_functions()
        self.host = Host(client_ip, self, client)
        self.server.register_instance(self.host)
        self.listen_thread = None
        self.listen_thread = threading.Thread(target=self._run)
        self.listen_thread.start()

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
        logger.debug("Start listening %s:%d" % self.server.server_address)
        self.server.serve_forever()
        logger.debug('Stop listening %s:%d' % self.server.server_address)

    def set_player(self, player):
        self.player = player

    def notify_start_game(self, **kwargs):
        self.player.start_game(kwargs)

    def notify_people_changed(self, **kwargs):
        self.player.people_changed(kwargs)

    def notify_sudoku_solved(self, **kwargs):
        self.player.sudoku_solved(kwargs)

    def notify_sudoku_changed(self, **kwargs):
        self.player.sudoku_changed(kwargs)

    def shutdown(self):
        self.server.shutdown()

    def leave_room_remove(self):
        self.client.leave_room_remove()