from common.listener import Listener, handler


class QueueListener(Listener):
    """
    Base class for classes that listen to events on in_queue
    methods of subclass decorated with @handler will be called when in_queue receives some event
    """

    def __init__(self, in_queue):
        super(QueueListener, self).__init__()
        self.in_queue = in_queue

    def handle_queue_event(self, block):
        event, args, kwargs = self.in_queue.get(block)
        self.handle_event(event, *args, **kwargs)




