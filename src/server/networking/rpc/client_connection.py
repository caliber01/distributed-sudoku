from common.networking import send, request
from server.networking.client_connection import ClientConnection
from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import logging

logger = logging.getLogger(__name__)

# TODO TERMINATE

class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class RPCClientConnection(ClientConnection):
    def __init__(self, client_ip):
        super(RPCClientConnection, self).__init__()
        self.client_ip = client_ip
        self.server = SimpleXMLRPCServer(('0.0.0.0', 0))
        self.proxy = None

    def register_functions(self, obj):
        self.server.register_introspection_functions()
        self.server.register_instance(obj)

    def listen(self):
        try:
            logger.debug("Start listening %s:%d" % self.server.server_address)
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C")
        finally:
            self.server.shutdown()
            self.server.server_close()

    def terminate(self):
        logger.debug("Shutdown RPC on %s:%d" % self.server.server_address)
        self.server.shutdown()
        self.server.server_close()

    def respond(self, type, **kwargs):
        try:
            send(self.socket, type=type, **kwargs)
        except:
            logger.debug("Exception occurs in client %s" % (self.name))

    def open_notifications_connection(self, port):
        self.proxy = ServerProxy("http://%s:%d" % (self.client_ip, port))

    def notify(self, type, **kwargs):
        return request(self.s_to_client, type=type, **kwargs)