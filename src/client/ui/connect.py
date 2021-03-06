from Tkinter import *
import re
import tkMessageBox
import ttk
import common.protocol as protocol


CONNECT = '<<connect>>'
HOST = '<<host>>'

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

        self._servers = []
        self._servers_var = StringVar()

        self.create_widgets()
        self.grid(row=0, column=0, padx=40, pady=40)

    def create_widgets(self):
        """
        creates widget in connection frame
        it contains a form where user need to fill in address and port
        """
        self._host_label = Label(self, text='Host local game')
        self._host_label.grid(row=0, columnspan=3)

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

        self._host_button = Button(self, text='Host', command=self.host)
        self._host_button.grid(row=4, columnspan=3, pady=20, sticky='ew')

        self._connect_label = Label(self, text='Existing servers')
        self._connect_label.grid(row=5, columnspan=3, pady=40)

        self._servers_list = Listbox(self, listvariable=self._servers_var)
        self._servers_list.grid(row=6, columnspan=3, ipadx=10, ipady=10)

        self._button_continue = Button(self, text='Connect', command=self.connect)
        self._button_continue.grid(row=7, columnspan=3, pady=20, sticky='ew')

    def set_servers(self, servers):
        self._servers = servers
        self._servers_var.set(' '.join(servers))

    def host(self):
        self.address = self._address_entry.get()
        self.port = self._port_entry.get()
        if re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', self.address) is None:
            tkMessageBox.showinfo('IP', 'Please check the validity of IP')
            return
        if not self.port or 1024 > int(self.port) or int(self.port) > 65535:
            tkMessageBox.showinfo('Port', 'Please check the validity of the port')
            return
        self.event_generate(HOST)

    def connect(self):
        """
        gets ip address and port that user submitted
        checks whether they are valid
        if they are, connects user to the game
        """
        selection = self._servers_list.curselection()
        if not len(selection):
            tkMessageBox.showerror("No room selected", "Please select a room")
            return
        server = self._servers[selection[0]]
        print(server)
        self.address, self.port = server.split(':')
        self.event_generate(CONNECT)
