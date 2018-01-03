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
from client.networking.rpc.host import RPCHost
from client.networking.indirect.connection import IndirectConnection
from client.networking.manual_host import ManualHost


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Distributed Sudoku 1.0')
    client_logic_queue = EventQueue()
    gui_queue = EventQueue()

    if arguments['--tcp']:
        host = ManualHost(TCPConnection(gui_queue))
    elif arguments['--rpc']:
        host = RPCHost()
    elif arguments['--indirect']:
        host = ManualHost(IndirectConnection(gui_queue))
    else:
        raise ValueError()

    client_logic = ClientLogic(client_logic_queue, gui_queue, host)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()
    client_logic_queue.publish(events.QUIT)


