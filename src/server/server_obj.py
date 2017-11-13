import socket
from threading import Thread
from common.constants import MESSAGE_SIZE, CLIENT_PORT
import server.client_handler
from common.listener import  Listener
from server.room_manager import RoomManager

class Server(Listener):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = {}
        self.room_manager = RoomManager()


    def create_room(self):
        return 1


    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen(10000)
        while True:
            client_socket, endpoint = self.s.accept()
            client = server.client_handler.ClientHandler(client_socket, self.room_manager)
            self.clients[id] = client
            t = Thread(target = client.run)
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
        # parts = message.split(MSG_SEP)
        # if parts[0] not in self.clients and parts[1] == INIT_SESSION:
        #
        #     handler = server.client_handler.ClientHandler(id, endpoint)
        #     self.__set_client_id(endpoint[0], id)
        # else:
        #     getattr(self.clients[parts[0]], parts[1])(parts[2:])


    def __set_client_id(self, ip, id):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, CLIENT_PORT))
        #s.send((SET_ID + MSG_SEP + id).encode())
        s.close()
