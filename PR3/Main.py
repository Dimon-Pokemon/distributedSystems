import threading

from UserInterface import UserInterface
from tkinter import *


class Main:
    client = None
    userInterface: UserInterface = None

    def __init__(self):
        self.userInterface = UserInterface(self)

    def start(self):
        self.userInterface.start_window_create_or_connect_to_chat()

    def update_listBox(self, name):
        self.userInterface.list_box_connections.insert(0, name)

    def create_client_and_connect_to_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        """Метод получения введенных данных для создания клиента"""
        from Client import Client
        host = client_host
        port = client_port
        name = client_name

        self.client = Client(self, host, port, name)

        self.client.start_receive()

        self.client.connect((server_host, server_port))
    #
    # def restart(self, name):
    #     self.start()
    #     self.userInterface.show_error("Ошибка", "Пользователь с ником уже подключен")

    def сделать_так_чтобы_все_было_хорошо(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        self.create_client_and_connect_to_chat(client_host, client_port, client_name, server_host, server_port)
        self.userInterface.connectToChatWindow.destroy()
        self.userInterface.start_main_window(client_name, client_host, client_port)

if __name__ == "__main__":
    main = Main()
    # thread1 = threading.Thread(target=main.start)
    # thread1.start()
    main.start()
    print("hello")
