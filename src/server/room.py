from collections import defaultdict
from common.protocol import *
import threading

class Room(object):
    def __init__(self, name, max_users, logger):
        self._logger = logger
        LOG.info("Room \"%s\" created" % (name))
        self.lock = threading.Lock()
        self.name = name
        self.users = []
        self.scores = {}
        self.max_users = max_users
        self.game_started = False
        self.__board = [[0 for x in range(9)] for y in range(9)]
        self.__scores = defaultdict(lambda: 0)

    def full(self):
        return len(self.users) < self.max_users


    def add_client(self, client):
        self.lock.acuire()
        if not self.full():
            raise Exception
        self.users.append(client)
        if len(self.users) == self.max_users:
            self.game_started = True
            self.__generate_game()
            self.__send_notification(START_GAME, matrix=str(self.__test_sudoku()))
            #self.__send_notification(START_GAME, matrix = str(self.__board))
        else:
            self.__send_notification(PEOPLE_CHANGED,)
        self.lock.release()


    def remove_client(self, client):
        self.lock.acuire()
        self.users.remove(client)
        self.__people_changed_notification()
        self.lock.release()


    def set_value(self, x, y, value):
        self.lock.acuire()
        # TODO SET_VALUE
        # TODO CHANGE SCORE
        self.__send_notification(SUDOKU_CHANGED, x = x, y = y, value = value)
        self.lock.release()

    def get_score(self):
        return self.scores


    def __generate_game(self):
        self.__board = None


    def __test_sudoku(self):
        return  """
0 0 3 0 2 0 6 0 0
9 0 0 3 0 5 0 0 1
0 0 1 8 0 6 4 0 0
0 0 8 1 0 2 9 0 0
7 0 0 0 0 0 0 0 8
0 0 6 7 0 8 2 0 0
0 0 2 6 0 9 5 0 0
8 0 0 2 0 3 0 0 9
0 0 5 0 1 0 3 0 0
"""


    def __people_changed_notification(self):
        names = []
        for user in self.users:
            names.append(user.name)
        self.__send_notification(PEOPLE_CHANGED, players = names, room_name = self.name, max_users = self.max_users, need_users = (self.max_users - len(names)))


    def __send_notification(self, type, **kargs):
        for user in self.users:
            user.send_notification(type, **kargs)