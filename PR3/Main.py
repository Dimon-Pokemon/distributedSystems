import threading

from UserInterface import UserInterface
from Client import Client
from tkinter import *


class Main:
    client: Client = None
    userInterface: UserInterface = None

    def __init__(self):
        self.userInterface = UserInterface(self)

    def start(self):
        self.userInterface.start_window_create_or_connect_to_chat()

    def create_client_and_connect_to_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        """Метод получения введенных данных для создания клиента"""
        host = client_host
        port = client_port
        name = client_name

        self.client = Client(host, port, name)

        self.client.start_receive()

        self.client.connect((server_host, server_port))
        # print("Method receive work!")

        # self.userInterface.connectToChatWindow.destroy()

        # print("Method destroy is working!")


if __name__ == "__main__":
    main = Main()
    # thread1 = threading.Thread(target=main.start)
    # thread1.start()
    main.start()
    print("hello")
