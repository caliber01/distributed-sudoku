from common.eventemitter import EventEmitter
from client.gui import UI
from client.networking import ServerConnector

if __name__ == '__main__':
    event_emitter = EventEmitter()

    server_connector = ServerConnector(event_emitter)
    ui = UI(event_emitter)

    ui.render_welcome()


