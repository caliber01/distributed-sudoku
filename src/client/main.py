"""Distributed Sudoku

Usage:
  client.py (--tcp | --rpc | --indirect)
  client.py (-h | --help)
  client.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --tcp         Use TCP sockets for networking
  --rpc         Use RPC for networking
  --indirect    Use indirect communication for networking

"""
from docopt import docopt
from client.gui import UI
from client.logic import ClientLogic
import client.events as events
from common.eventqueue import EventQueue
from client.networking.tcp.connection import TCPConnection
from client.networking.rpc.connection import RPCConnection
from client.networking.indirect.connection import IndirectConnection

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Distributed Sudoku 1.0')
    client_logic_queue = EventQueue()
    gui_queue = EventQueue()

    if arguments['--tcp']:
        connection = TCPConnection(gui_queue)
    elif arguments['--rpc']:
        connection = RPCConnection(gui_queue)
    elif arguments['--indirect']:
        connection = IndirectConnection(gui_queue)
    else:
        raise ValueError()

    client_logic = ClientLogic(client_logic_queue, gui_queue, connection)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()
    client_logic_queue.publish(events.QUIT)


