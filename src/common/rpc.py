from SimpleXMLRPCServer import SimpleXMLRPCServer


class CustomXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, addr, **kwargs):
        SimpleXMLRPCServer.__init__(self, addr, **kwargs)
        self.should_shutdown = False

    def serve_forever(self, poll_interval=0.5):
        while not self.should_shutdown:
            self.handle_request()

    def shutdown(self):
        self.should_shutdown = True
