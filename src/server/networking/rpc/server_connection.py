import socket
import logging
from server.networking.rpc.client_proxy import RPCClientProxy
from server.networking.server_connection import ServerConnection

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


logger = logging.getLogger(__name__)


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class ConnectionsHandler(object):
    def __init__(self, client_handler_factory, on_connection):
        self.client_handler_factory = client_handler_factory
        self.on_connection = on_connection

    def connect(self, ip):
        logger.debug('Created client handler for  %s' % ip)
        client_handler = self.client_handler_factory()
        client = RPCClientProxy(client_handler, ip)
        self.on_connection(client)


class RPCServerConnection(ServerConnection):
    def __init__(self, ip, port, client_handler_factory):
        self.client_handler_factory = client_handler_factory
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def accept_connections(self, on_connection):
        handler = ConnectionsHandler(on_connection, self.client_handler_factory)
        endpoint = (self.ip, self.port)
        server = SimpleXMLRPCServer(endpoint, requestHandler=RPCHandler)
        server.register_introspection_functions()
        server.register_instance(handler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C")
        finally:
            server.shutdown()
            server.server_close()