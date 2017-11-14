from client.gui import UI
from client.logic import ClientLogic
import client.events as events
import common.protocol as protocol
from common.eventqueue import EventQueue
from client.notifications import NotificationsConnection

if __name__ == '__main__':
    notifications_connection_queue = EventQueue()
    client_logic_queue = EventQueue()
    gui_queue = EventQueue()

    notifications_connection = NotificationsConnection(notifications_connection_queue, gui_queue)
    client_logic = ClientLogic(client_logic_queue, gui_queue, notifications_connection.port)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()
    client_logic_queue.publish(events.QUIT)
    notifications_connection_queue.publish(events.QUIT)

    # client_logic_queue.publish(events.CONNECT_TO_SERVER, ("127.0.0.1", protocol.DEFAULT_PORT))
    # client_logic_queue.publish(events.CREATE_ROOM, name="NAME", max_users = 120)


