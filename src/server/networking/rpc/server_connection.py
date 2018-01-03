import socket
import logging
from server.networking.rpc.client_connection import RPCClientConnection
from server.networking.server_connection import ServerConnection

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


logger = logging.getLogger(__name__)

class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class Handler(object):
    def __init__(self, on_connection):
        self.on_connection = on_connection

    def connect(self, ip):
        logger.debug('Created client handler for  %s' % ip)
        connection = RPCClientConnection(ip)
        self.on_connection(connection)
        return connection.server.server_address[1]


class RPCServerConnection(ServerConnection):
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def accept_connections(self, on_connection):
        handler = Handler(on_connection)
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