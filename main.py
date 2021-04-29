import tkinter as tk
import tkinter.messagebox as tk_messagebox
import re

from pong_protocol.client import get_protocol_client
from pong_protocol.server import get_protocol_server

IP_ADDRESS_PATTERN = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'


class MainMenu(tk.Frame):
    def __init__(self, master):
        super(MainMenu, self).__init__(master)
        self.master = master
        self.ip_address_input_string = tk.StringVar(master)
        self.ip_address = None
        self.is_server = None
        self.pack()
        self.server_button = tk.Button(self, text='open server', command=self.open_server)
        self.server_button.pack(side='top')

        self.ip_input = tk.Entry(self, textvariable=self.ip_address_input_string)
        self.ip_input.pack(side='bottom')

        self.client_button = tk.Button(self, text='join server', command=self.join_server)
        self.client_button.pack(side='bottom')

    def stop_app(self):
        self.destroy()
        self.master.destroy()

    def join_server(self):
        self.is_server = False
        self.ip_address = self.ip_address_input_string.get()
        if re.match(IP_ADDRESS_PATTERN, self.ip_address) and \
                all([int(num) < 256 for num in self.ip_address.split('.')]):
            self.stop_app()

        else:
            reply = tk_messagebox.askokcancel(self, message='ip address is wrong. Is it a DNS?')
            if reply:
                self.stop_app()

    def open_server(self):
        self.is_server = True
        self.destroy()
        self.master.destroy()


def main():
    root = tk.Tk()
    app = MainMenu(master=root)
    app.mainloop()
    print(f'{app.is_server=} {app.ip_address=}')

    if app.is_server:
        get_protocol_server()
    else:
        get_protocol_client(app.ip_address)

if __name__ == '__main__':
    main()
