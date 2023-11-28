import threading

from UserInterface import UserInterface
from Message import Message
from Status import Status
# from tkinter import *


class Main:
    client = None
    userInterface: UserInterface = None
    chats_history: dict = {}
    selected_chat: str = None

    def __init__(self):
        self.userInterface = UserInterface(self)

    def start(self):
        self.userInterface.start_window_create_or_connect_to_chat()

    def update_listBox(self, name):
        self.userInterface.list_box_connections.insert(0, name)

    def set_selected_chat(self, name):
        self.selected_chat = name

    def get_chat_history(self, name: str):
        return self.chats_history[name]

    def send(self, to_name, text_message):
        message = Message(
            status=Status.MESSAGE.value,
            position='right',
            to_name=to_name,
            from_name=self.client.name,
            text=text_message
        )
        self.chats_history[to_name].append(message)
        self.userInterface.print_message(message)
        self.client.send(to_name, message)

    def print_new_message_from_client(self, text_message, name):
        message = Message(
            position='left',
            text=text_message
        )
        print(self.chats_history)
        self.chats_history[name].append(message)
        self.userInterface.print_message(message)

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
