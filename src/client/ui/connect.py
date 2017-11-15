from Tkinter import *
import re
import tkMessageBox
import ttk
import common.protocol as protocol


CONNECT = '<<connect>>'

def validate_address(address):
    """
    checks if entered address is valid
    """
    return bool(re.match(r'^(?:[0-9]{0,3})(?:\.[0-9]{0,3}){0,3}$', address))


def validate_port(port):
    """
    checks if entered port is valid
    """
    return not port or bool(re.match(r'^[0-9]+$', port)) and int(port) < 65536


class Connect(Frame):
    def __init__(self, master=None, **kw):
        """
        creates connection frame that is the first that user sees
        """
        Frame.__init__(self, master, **kw)
        self.ips = {'127.0.0.1'}
        self.ports = {protocol.DEFAULT_PORT}
        self.address = ""
        self.port = ""
        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        """
        creates widget in connection frame
        it contains a form where user need to fill in address and port
        """
        self._main_label = Label(self, text='Please specify server address')
        self._main_label.grid(row=0, columnspan=3)

        self._address_label = Label(self, text='IP:')
        self._address_label.grid(row=1, pady=20)

        validate_address_command = self.register(validate_address)
        self._address_entry = ttk.Combobox(self, values=list(self.ips), validate='all', validatecommand=(validate_address_command, '%P'))
        self._address_entry.grid(row=1, column=1, columnspan=2)

        validate_port_command = self.register(validate_port)
        self._port_label = Label(self, text='Port:')
        self._port_label.grid(row=2)

        self._port_entry = ttk.Combobox(self, values=list(self.ports), validate='all', validatecommand=(validate_port_command, '%P'))
        self._port_entry.grid(row=2, column=1, columnspan=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self._button_continue = Button(self, text='Connect', command=self.submit)
        self._button_continue.grid(row=4, column=1, pady=20, sticky='ew')

    def submit(self):
        """
        gets ip address and port that user submitted
        checks whether they are valid
        if they are, connects user to the game
        """
        self.address = self._address_entry.get()
        self.port = self._port_entry.get()
        if re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', self.address) is None:
            tkMessageBox.showinfo('IP', 'Please check the validity of IP')
            return
        if not self.port or 1024 > int(self.port) or int(self.port) > 65535:
            tkMessageBox.showinfo('Port', 'Please check the validity of the port')
            return
        self.event_generate(CONNECT)
