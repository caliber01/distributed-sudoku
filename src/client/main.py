import logging.config

logging.config.fileConfig('logger.conf')

from client.gui import UI
from client.logic import ClientLogic
from queue import Queue
import client.events as events
import common.protocol as protocol

if __name__ == '__main__':
    client_logic_queue = Queue()
    gui_queue = Queue()

    client_logic = ClientLogic(client_logic_queue, gui_queue)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()

    # TODO: remove hardcode
    client_logic_queue.put((events.CONNECT_TO_SERVER, ("127.0.0.1", protocol.DEFAULT_PORT)))


