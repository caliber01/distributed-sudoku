import client.events as events
from threading import Thread, Lock
from common.constants import MESSAGE_SIZE, CLIENT_PORT
import socket
from common.messages import *

class ServerConnector(object):
    def __init__(self, event_emitter, endpoint):
        self.event_emitter = event_emitter
        self.endpoint = endpoint
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind(("127.0.0.1", CLIENT_PORT))
        self.__lock = Lock()
        self.id = ""
        # Start listening first for retrieving the client id
        self.__l_tread = Thread(target=self.__listen)
        self.__l_tread.start()
        # Start session on server
        self.__init_session()
        event_emitter.subscribe(events.SUBMIT_NICKNAME, self.submit_nickname)
        event_emitter.subscribe(events.MESSAGE, self.message)


    def submit_nickname(self, nickname):
        print(nickname)


    # TODO Example. Remove later
    def message(self, message):
        self.__send_message(PRINT_MESSAGE + ":" + message)


    def start_listening(self):
        self.__thread.start()


    def stop_listening(self):
        # TODO
        print("not implemented")


    # Call for sending message to server
    def __send_message(self, message):
        self.__lock.acquire()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.endpoint)
            s.send((self.id + ":" + message).encode())
            s.close()
        except:
            # TODO Display error message
            print("TROLOLO")
        finally:
            self.__lock.release()


    def __init_session(self):
        # TODO TRY CATCH IMPORTANT
        self.__send_message(INIT_SESSION)
        self.__lock.acquire()


    def __listen(self):
        self.__s.listen(1)
        while True:
            sock, endpoint = self.__s.accept()
            message = ""
            while True:
                m = sock.recv(MESSAGE_SIZE).decode()
                if not len(m):
                    break
                message += m
            sock.close()
            parts = message.split(":")
            getattr(self, parts[0])(parts[1:])


    def set_id(self, id):
        self.id = id[0]
        self.__lock.release()