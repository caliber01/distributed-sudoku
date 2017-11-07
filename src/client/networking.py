import client.events as events


class ServerConnector(object):
    def __init__(self, event_emitter):
        self.event_emitter = event_emitter
        event_emitter.subscribe(events.SUBMIT_NICKNAME, self.submit_nickname)

    def submit_nickname(self, nickname):
        print(nickname)
