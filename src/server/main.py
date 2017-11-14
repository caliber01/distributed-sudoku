from server.server_obj import Server
from common.protocol import DEFAULT_PORT
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
    # Starting server
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    server = Server('127.0.0.1', DEFAULT_PORT)
    server.run()
