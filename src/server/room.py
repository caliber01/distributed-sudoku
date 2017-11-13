class Room(object):
    def __init__(self, name, max_users):
        self.name = name
        self.users = []
        self.scores = {}
        self.max_users = max_users
        self.game_started = False

    def place_exists(self):
        return len(self.users) < self.max_users

    def add_client(self, client):
        if not self.place_exists():
            raise Exception
        self.users.append(client)
        #if not game_starged:
        # TODO notification

    def remove_client(self, client):
        self.users.remove(client)
        # if not game_starged:
        # TODO notification
