class ClientConnection(object):
    def __init__(self):
        self.name = None

    def set_name(self, name):
        self.name = name

    def listen(self, on_message, on_terminate):
        raise NotImplementedError()

    def respond(self, type, **kwargs):
        raise NotImplementedError()

    def open_notifications_connection(self, args):
        raise NotImplementedError()

    def notify(self, type, **kwargs):
        raise NotImplementedError()
