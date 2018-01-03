from client.networking.host import Host
from xmlrpclib import ServerProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import common.protocol as protocol
import socket
import threading


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RPCHost(Host):
    def __init__(self, out_queue):
        self.proxy = None
        self.server = None
        self.listen_thread = None
        self.server_port = None
        self.out_queue = out_queue

    def connect(self, server):
        self.proxy = ServerProxy("http://%s:%d" % server)
        self.server_port = self.proxy.connect(socket.gethostbyname(socket.gethostname()))
        self.proxy = ServerProxy("http://%s:%d" % (server[0], self.server_port))
        self.server = SimpleXMLRPCServer(("0.0.0.0", 0), requestHandler=RPCHandler)
        self.server.register_introspection_functions()
        self.server.register_instance(self)
        self.listen_thread = threading.Thread(target=self.run)
        self.listen_thread.start()
        self.proxy.send_client_port(self.server.server_address[1])

    def run(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C")
        finally:
            self.server.shutdown()
            self.server.server_close()

    def set_name(self, name):
        self.proxy.set_name(name)

    def load_rooms(self):
        return self.proxy.get_available_rooms()

    def join_game(self, id):
        code, args = self.proxy.join_to_room(id)
        if code != protocol.RESPONSE_OK:
            raise ValueError()
        return args

    def create_room(self, name, max_users):
        code, args = self.proxy.create_room(name, max_users)
        return args

    def cell_edited(self, x, y, prev_value, new_value):
        return self.proxy.set_sudoku_value(x, y, new_value, prev_value)

    def leave_room(self):
        return self.proxy.leave_room()

    def shutdown(self):
        self.proxy.terminate()
        self.server.shutdown()
        self.server.server_close()

    def _request(self, **kwargs):
        pass

    def start_game(self, args):
        self.out_queue.publish(protocol.START_GAME, **args)
        return protocol.RESPONSE_OK

    def people_changed(self, args):
        self.out_queue.publish(protocol.PEOPLE_CHANGED, **args)
        return protocol.RESPONSE_OK

    def sudoku_solved(self, args):
        self.out_queue.publish(protocol.SUDOKU_SOLVED, **args)
        return protocol.RESPONSE_OK

    def sudoku_changed(self, args):
        self.out_queue.publish(protocol.SUDOKU_CHANGED, **args)
        return protocol.RESPONSE_OK