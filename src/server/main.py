from server.server_obj import Server
from common.protocol import DEFAULT_PORT, DEFAULT_SERVER_INET_ADDR
from argparse import ArgumentParser # Parsing command line arguments
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

if __name__ == '__main__':
    parser = ArgumentParser(description=__info())
    parser.add_argument('-l', '--listenaddr', help='Bind server socket to INET address, defaults to %s' % DEFAULT_SERVER_INET_ADDR, default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p', '--listenport', help='Bind server socket to TCP port, defaults to %d' % DEFAULT_PORT, default=DEFAULT_PORT)
    args = parser.parse_args()
    # Starting server
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    server = Server(args.listenaddr, int(args.listenport), LOG)
    server.run()
