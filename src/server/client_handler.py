from common.constants import MESSAGE_SIZE

class ClientHandler(object):
    def __init__(self, id, endpoint):
        self.id = id
        self.endpoint = endpoint

    # Example
    def print_message(self, args):
        print(args[0])
