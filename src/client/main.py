from client.gui import UI
from client.logic import ClientLogic
from queue import Queue

if __name__ == '__main__':
    client_logic_queue = Queue()
    gui_queue = Queue()

    client_logic = ClientLogic(client_logic_queue, gui_queue)
    ui = UI(gui_queue, client_logic_queue)

    ui.render_welcome()


