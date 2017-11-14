from collections import defaultdict
from common.protocol import START_GAME

class Room(object):
    def __init__(self, name, max_users):
        self.name = name
        self.users = []
        self.scores = {}
        self.max_users = max_users
        self.game_started = False
        self.__board = [[0 for x in range(9)] for y in range(9)]
        self.__scores = defaultdict(0)

    def place_exists(self):
        return len(self.users) < self.max_users

    def add_client(self, client):
        if not self.place_exists():
            raise Exception
        self.users.append(client)
        if len(self.users) == self.max_users:
            self.game_started = True
            self.__generate_game()

        #if not game_starged:
        # TODO notification

    def remove_client(self, client):
        self.users.remove(client)
        # if not game_starged:
        # TODO notification


    def __generate_game(self):
        # TODO
        return


    def __send_notification(self, type, **kargs):
        for user in self.users:
            user.send_notification(START_GAME, matrix = self.__board)