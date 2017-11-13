from client.gui import UI
from client.logic import ClientLogic
import client.events as events
import common.protocol as protocol
from common.eventqueue import EventQueue
from client.notifications import NotificationsConnection

if __name__ == '__main__':
    client_logic_queue = EventQueue()
    gui_queue = EventQueue()

    notifications_connection = NotificationsConnection(client_logic_queue)
    client_logic = ClientLogic(client_logic_queue, gui_queue, notifications_connection.port)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()

    # TODO: remove hardcode
    client_logic_queue.publish(events.CONNECT_TO_SERVER, ("127.0.0.1", protocol.DEFAULT_PORT))


