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
    def __init__(self):
        self.handlers = defaultdict(list)
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'handled_event'):
                self.handlers[attr.handled_event].append(attr)

    def handle_event(self, event, *args, **kwargs):
        for event_handler in self.handlers[event]:
            return event_handler(*args, **kwargs)
