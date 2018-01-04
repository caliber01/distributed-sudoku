from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import common.protocol as protocol
from threading import Thread


class RPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Player(Thread):
    def __init__(self, gui_queue):
        super(Player, self).__init__(target=self.run)
        self.gui_queue = gui_queue
        self.server = SimpleXMLRPCServer(("0.0.0.0", 0), requestHandler=RPCHandler)
        self.server.register_introspection_functions()
        self.server.register_instance(self)

    def run(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C")
        finally:
            self.server.shutdown()
            self.server.server_close()

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
