import socket
from threading import Thread
from common.constants import MESSAGE_SIZE, CLIENT_PORT
import server.client_handler
from common.listener import  Listener
from server.room_manager import RoomManager
from server.main import LOG

class Server(Listener):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = {}
        self.room_manager = RoomManager()


    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOG.debug('Server socket created, descriptor %d' % self.s.fileno())
        self.s.bind((self.ip, self.port))
        LOG.debug('Server socket bound on %s:%d' % self.s.getsockname())
        LOG.info('Accepting requests on TCP %s:%d' % self.s.getsockname())
        self.s.listen(10000)
        try:
            while True:
                LOG.debug('Awaiting requests ...')
                client_socket, endpoint = self.s.accept()
                LOG.debug('Created cliend handler for  %s:%d' % client_socket.getsockname())
                client = server.client_handler.ClientHandler(client_socket, self.room_manager)
                self.clients[id] = client
                t = Thread(target=client.run)
                t.start()
            s.close()
        except e:
            LOG.info('Exception occurs %s' % (s))