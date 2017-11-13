from server.server_obj import Server
from common.protocol import DEFAULT_PORT

if __name__ == '__main__':
    server = Server('127.0.0.1', DEFAULT_PORT)
    server.run()
