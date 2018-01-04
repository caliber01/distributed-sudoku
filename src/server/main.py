from server.networking.protocol.tcp.server_connection import TCPServerConnection
from server.networking.rpc.server_connection import RPCServerConnection
from server.room_manager import RoomManager
from server.server_types import *
from server.broadcast import start_broadcasting
from common.protocol import DEFAULT_PORT, DEFAULT_SERVER_INET_ADDR
from argparse import ArgumentParser
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()

# Constants -------------------------------------------------------------------
___NAME = 'Sudoku'
___VER = '0.0.0.1'
___DESC = 'Sudoku'
___BUILT = '2017-11-14'
___VENDOR = 'Copyright (c) Anton Potapchuk, Diana Grigoryan, Yevgenia Krivenko, Maxim Semikin'

def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)


def serve(server_type, addr=DEFAULT_SERVER_INET_ADDR, port=DEFAULT_PORT, shutdown_event=None):
    room_manager = RoomManager()

    if server_type == TCP:
        server_connection = TCPServerConnection(addr, int(port), room_manager)
    elif server_type == RPC:
        server_connection = RPCServerConnection(addr, int(port), room_manager)
    elif server_type == INDIRECT:
        server_connection = None
    else:
        raise ValueError()

    start_broadcasting('{}:{}'.format(addr, port))
    server_connection.accept_connections(shutdown_event)


if __name__ == '__main__':
    parser = ArgumentParser(description=__info())
    parser.add_argument('-l', '--listenaddr', help='Bind server socket to INET address, defaults to %s' % DEFAULT_SERVER_INET_ADDR, default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p', '--listenport', help='Bind server socket to TCP port, defaults to %d' % DEFAULT_PORT, default=DEFAULT_PORT)
    parser.add_argument('-t', '--type', help='Server type: tcp), rpc, indirect', default=TCP)

    args = parser.parse_args()

    if args.type != TCP and args.type != RPC and args.type != INDIRECT:
        print("Unknown server type. Server type should be %s or %s or %s." % (TCP, RPC, INDIRECT))
        exit(-1)

    # Starting server
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    LOG.info('Using {}'.format(args.type))
    serve(args.type, args.listenaddr, args.listenport)
