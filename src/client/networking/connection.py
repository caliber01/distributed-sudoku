class Connection():
    def __init__(self, out_queue):
        '''
        :param out_queue: queue to publish updates pushed from server
        '''
        self.out_queue = out_queue

    def shutdown(self):
        raise NotImplementedError()

    def connect(self, server):
        '''
        :param server: server address
        :return: port of local listening socket
        '''
        raise NotImplementedError()

    def blocking_request(self, type, **kwargs):
        raise NotImplementedError()
