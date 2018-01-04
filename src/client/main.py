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
from client.middleware import Middleware
from common.eventqueue import EventQueue
from client.networking.tcp.connection import TCPConnection
from client.networking.rpc.host import RPCHost
from client.networking.indirect.connection import IndirectConnection
from client.networking.manual_host import ManualHost
from server.server_types import *
import logging


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Distributed Sudoku 1.0')
    requests_queue = EventQueue()
    gui_queue = EventQueue()

    if arguments['--tcp']:
        logger.info('Using TCP')
        host = ManualHost(TCPConnection(gui_queue))
        server_type = TCP
    elif arguments['--rpc']:
        logger.info('Using RPC')
        host = RPCHost(gui_queue)
        server_type = RPC
    elif arguments['--indirect']:
        logger.info('Using Indirect Communication')
        host = ManualHost(IndirectConnection(gui_queue))
        server_type = INDIRECT
    else:
        raise ValueError()

    middleware = Middleware(requests_queue, gui_queue, host, server_type)
    ui = UI(gui_queue, requests_queue)

    ui.render_welcome()
    middleware.shutdown()


