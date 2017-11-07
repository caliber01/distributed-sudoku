from collections import defaultdict

class EventEmitter(object):
    def __init__(self):
        self._subscriptions = defaultdict(list)

    def subscribe(self, event, handler):
        self._subscriptions[event].append(handler)

    def publish(self, event, *args, **kargs):
        for handler in self._subscriptions[event]:
            handler(*args, **kargs)


