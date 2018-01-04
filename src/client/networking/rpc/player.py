from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from common.rpc import CustomXMLRPCServer
import common.protocol as protocol
from threading import Thread


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Player(Thread):
    def __init__(self, gui_queue):
        super(Player, self).__init__(target=self.run)
        self.gui_queue = gui_queue
        self.server = CustomXMLRPCServer(("0.0.0.0", 0), requestHandler=RPCHandler, allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_instance(self)

    def run(self):
        self.server.serve_forever()

    def start_game(self, args):
        self.gui_queue.publish(protocol.START_GAME, **args)
        return protocol.RESPONSE_OK

    def people_changed(self, args):
        self.gui_queue.publish(protocol.PEOPLE_CHANGED, **args)
        return protocol.RESPONSE_OK

    def sudoku_solved(self, args):
        self.gui_queue.publish(protocol.SUDOKU_SOLVED, **args)
        return protocol.RESPONSE_OK

    def sudoku_changed(self, args):
        self.gui_queue.publish(protocol.SUDOKU_CHANGED, **args)
        return protocol.RESPONSE_OK

    def get_address(self):
        return self.server.server_address[1]

    def terminate(self):
        self.server.shutdown()

