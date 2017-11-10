from common.eventemitter import EventEmitter
from client.gui import UI
from client.networking import ServerConnector

if __name__ == '__main__':
    event_emitter = EventEmitter()
    # TODO ServerPort
    server_connector = ServerConnector(event_emitter, ("127.0.0.1", 6345))
    ui = UI(event_emitter)

    ui.render_welcome()


