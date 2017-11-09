from queue import Queue


class EventQueue(Queue):
    def publish(self, event, *args, **kargs):
        self.put((event, args, kargs))
