import socket
from threading import Thread
from common.constants import MESSAGE_SIZE, CLIENT_PORT
from common.messages import INIT_SESSION, SET_ID
import server.client_handler
import uuid

class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = {}

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(10000)
        while True:
            client_socket, endpoint = self.s.accept()
            t = Thread(target = self.__process_client_request, args=(client_socket, endpoint))
            t.start()
        s.close()


    def __process_client_request(self, s, endpoint):
        message = ""
        while True:
            m = s.recv(MESSAGE_SIZE)
            if not len(m):
                break
            message += m.decode()
        s.close()
        if not len(message):
            return
        parts = message.split(":")
        if parts[0] not in self.clients and parts[1] == INIT_SESSION:
            id = str(uuid.uuid1())
            handler = server.client_handler.ClientHandler(id, endpoint)
            self.clients[id] = handler
            self.__set_client_id(endpoint[0], id)
        else:
            getattr(self.clients[parts[0]], parts[1])(parts[2:])


    def __set_client_id(self, ip, id):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, CLIENT_PORT))
        s.send((SET_ID + ":" + id).encode())
        s.close()
