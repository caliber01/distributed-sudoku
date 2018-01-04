import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
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

    def leave_room_remove(self, **kwargs):
        return self.client.leave_room_remove(**kwargs)

    def set_sudoku_value(self, **kwargs):
        return self.client.set_sudoku_value(**kwargs)

    def set_name(self, **kwargs):
        return self.client.set_name(**kwargs)

    def join_to_room(self, **kwargs):
        return self.client.join_to_room(**kwargs)

    def create_room(self, **kwargs):
        return self.client.create_room(**kwargs)

    def get_available_rooms(self, **kwargs):
        return self.client.get_available_rooms(**kwargs)

    def leave_room(self, **kwargs):
        return self.client.leave_room(**kwargs)


# TODO stop
class RPCClientProxy(ClientProxy):
    def __init__(self, client, client_ip):
        super(RPCClientProxy, self).__init__()
        self.client = client
        self.client_ip = client_ip
        self.player = None
        self.host = Host(client_ip, self, client)
        self.server = SimpleXMLRPCServer(('0.0.0.0', 0))
        self.server.register_introspection_functions()
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
        try:
            logger.debug("Start listening %s:%d" % self.server.server_address)
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C")
        finally:
            self.server.shutdown()
            self.server.server_close()

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