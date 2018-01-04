from collections import defaultdict
from server.sudoku import Sudoku
from common.errors import *
import threading
import uuid

import logging

logger = logging.getLogger(__name__)


class Room(object):
    def __init__(self, name, max_users):
        """
        creates new game
        """
        self.id = str(uuid.uuid1())
        logger.info("Room \"%s\" created" % (name))
        self.lock = threading.Lock()
        self.name = name
        self.users = []
        self.scores = {}
        self.max_users = max_users
        self.game_started = False
        self.__sudoku = Sudoku(0.6)
        self.__scores = defaultdict(lambda: 0)

    def full(self):
        """
        checks if the game has all the users it needs
        """
        return len(self.users) == self.max_users

    def add_client(self, client):
        """
        adds new user to the game
        """
        with self.lock:
            if self.full():
                raise FullRoomError()
            self.users.append(client)
            if len(self.users) == self.max_users:
                self.game_started = True
                for user in self.users:
                    user.notify_start_game(matrix=str(self.__sudoku.print_matrix()))
            else:
                self.__people_changed_notification(ignore=client)

    def remove_client(self, client_id):
        """
        deletes user from the game
        """
        with self.lock:
            if client_id in [user.id for user in self.users]:
                self.users = [user for user in self.users if user.id != client_id]
                self.__people_changed_notification()
            if len(self.users) == 1:
                scores = [(self.users[0].name, self.__scores[self.users[0].id])]
                for user in self.users:
                    user.notify_sudoku_solved(scores=scores)
                self.users[0].leave_room_remove()

    def set_value(self, user_id, x, y, value, prev):
        with self.lock:
            if self.__sudoku.unsolved[x][y] != prev:
                raise TooLateError()
            if self.__sudoku.check(x, y, value):
                self.__scores[user_id] += 1
            else:
                self.__scores[user_id] -= 1
            self.__sudoku.unsolved[x][y] = value
            for user in self.users:
                if user.id is not user_id:
                    user.notify_sudoku_changed(x=x, y=y, value=value)

            if self.__is_sudoku_solved():
                score = []
                for user in self.users:
                    score.append((user.name, self.__scores[user.id]))
                for user in self.users:
                    user.notify_sudoku_solved(scores=score)

    def __is_sudoku_solved(self):
        for i in range(9):
            for j in range(9):
                if self.__sudoku.unsolved[i][j] != self.__sudoku.solved[i][j]:
                    return False
        return True

    def get_score(self):
        """
        returns list of users' scores
        """
        return self.scores

    def __people_changed_notification(self, ignore=None):
        """
        creates notification if list of users in a game changes
        """
        names = [user.name for user in self.users]

        for user in self.users:
            if user == ignore:
                continue
            user.notify_people_changed(users=names, room_name=self.name,
                                       max_users=self.max_users,
                                       need_users=(self.max_users - len(names)))

