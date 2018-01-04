class ServerConnection(object):
    def accept_connections(self, shutdown_event):
        raise NotImplementedError()
