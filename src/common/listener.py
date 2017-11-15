from collections import defaultdict


def handler(event):
    """
    Decorator to mark methods as handling events from the in_queue
    :param event: event type this method handles
    :return: wrapped method
    """
    def wrapper(method):
        method.handled_event = event
        return method
    return wrapper


class Listener(object):
    """
    Base class for classes that listen to events on in_queue
    methods of subclass decorated with @handler will be called when in_queue receives some event
    """

    def __init__(self, in_queue):
        self.in_queue = in_queue
        self.handlers = defaultdict(list)
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'handled_event'):
                self.handlers[attr.handled_event].append(attr)

    def handle_event(self, block):
        event, args, kargs = self.in_queue.get(block)
        for event_handler in self.handlers[event]:
            event_handler(*args, **kargs)




