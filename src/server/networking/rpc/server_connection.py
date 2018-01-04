import socket
import logging
from server.networking.rpc.client_proxy import RPCClientProxy
from server.networking.server_connection import ServerConnection
from server.client_handler import ClientHandler

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


logger = logging.getLogger(__name__)


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class ConnectionsHandler(object):
    def __init__(self, room_manager):
        self.room_manager = room_manager

    def connect(self, ip):
        logger.debug('Created client handler for  %s' % ip)
        client_handler = ClientHandler(self.room_manager)
        client = RPCClientProxy(client_handler, ip)
        self.room_manager.add_client(client)
        print(client.server.server_address[1])
        return client.server.server_address[1]


class RPCServerConnection(ServerConnection):
    def __init__(self, ip, port, room_manager):
        self.room_manager = room_manager
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def accept_connections(self, shutdown_event):
        handler = ConnectionsHandler(self.room_manager)
        endpoint = (self.ip, self.port)
        server = SimpleXMLRPCServer(endpoint, requestHandler=RPCHandler, allow_none=True)
        server.register_introspection_functions()
        server.register_instance(handler)
        if shutdown_event is None:
            server.serve_forever()
        else:
            server.timeout = 5
            while True:
                if shutdown_event.is_set():
                    server.shutdown()
                    return
                try:
                    server.handle_request()
                except socket.timeout:
                    continue


