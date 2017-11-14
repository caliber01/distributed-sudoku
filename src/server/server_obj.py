import socket
from threading import Thread
import server.client_handler
from common.listener import  Listener
from server.room_manager import RoomManager

class Server(Listener):
    def __init__(self, ip, port, logger):
        self.ip = ip
        self.port = port
        self.clients = {}
        self.logger = logger
        self.room_manager = RoomManager(self.logger)


    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('Server socket created, descriptor %d' % self.s.fileno())
        self.s.bind((self.ip, self.port))
        self.logger.debug('Server socket bound on %s:%d' % self.s.getsockname())
        self.logger.info('Accepting requests on TCP %s:%d' % self.s.getsockname())
        self.s.listen(10000)
        while True:
            try:
                self.logger.debug('Awaiting requests ...')
                client_socket, endpoint = self.s.accept()
                self.logger.debug('Created cliend handler for  %s:%d' % client_socket.getsockname())
                client = server.client_handler.ClientHandler(client_socket, self.room_manager, self.logger)
                self.clients[id] = client
                t = Thread(target=client.run)
                t.start()
            except:
                self.logger.info('Exception occurs in main thread')
        self.s.close()
