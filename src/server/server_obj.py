import socket
from threading import Thread
import server.client_handler

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
            handler = server.client_handler.ClientHandler(client_socket, endpoint)
            t = Thread(target = handler.run)
            t.start()
        s.close()