import socket
from server.client_handler import ClientHandler

class Server(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(10000)
        while True:
            client_socket, endpoint = self.s.accept()
            # TODO Thread
            handler = ClientHandler(client_socket)
        s.close()