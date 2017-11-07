import tkinter
import client.events as events


class UI(object):

    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

    def render_welcome(self):
        self.event_emitter.publish(events.SUBMIT_NICKNAME, "Mynickname")


