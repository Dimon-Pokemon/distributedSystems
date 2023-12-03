import os
import sys
import threading
import time
import tkinter

from UserInterface import UserInterface
from Message import Message
from Status import Status
# from tkinter import *


class Main:
    client = None
    userInterface: UserInterface = None
    chats_history: dict = {}
    selected_chat: str = None

    '''address_chat_node - это участник чата или сигнальный сервер. При запуске приложения мы указываем ip и port этого
     участника чата/сигнального сервера. К нему новый клиент обращается чтобы получить сведения о других
      участниках(клиентах) чата.'''
    address_chat_node = None # Может быть сервером или клиентом чата

    def __init__(self):
        self.userInterface = UserInterface(self)

    def start(self):
        self.userInterface.start_window_create_or_connect_to_chat()

    def update_listBox(self, name):
        self.userInterface.list_box_connections.insert(0, name)

    def set_selected_chat(self, name):
        self.selected_chat = name

    def delete_client(self, name_client_which_exit):
        # Удаление истории переписки с вышедшим клиентом
        self.chats_history.pop(name_client_which_exit)
        # Удаление вышедшего клиента из GUI
        self.userInterface.delete_name_from_listbox(name_client_which_exit)

    def exit(self):
        self.client.exit(self.address_chat_node) # Вызываем метод уведомления всех участникам чата о выходе клиента из чата
        sys.exit(0)

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
        self.chats_history[name].append(message)
        if name == self.selected_chat:
            self.userInterface.print_message(message)

    def create_client_and_connect_to_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        """Метод получения введенных данных для создания клиента"""
        from Client import Client
        host = client_host
        port = client_port
        name = client_name

        self.client = Client(self, host, port, name)

        self.client.start_receive()

        self.address_chat_node = (server_host, server_port)

        self.client.connect(self.address_chat_node)
    #
    # def restart(self, name):
    #     self.start()
    #     self.userInterface.show_error("Ошибка", "Пользователь с ником уже подключен")

    def create_client_and_start_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        self.create_client_and_connect_to_chat(client_host, client_port, client_name, server_host, server_port)
        self.userInterface.connectToChatWindow.destroy()
        self.userInterface.start_main_window(client_name, client_host, client_port)

    def create_server(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        thread = threading.Thread(target=os.system, daemon=True, args=[f"python3 Server.py --host {server_host} --port {server_port}"])
        thread.start()
        time.sleep(10) # Надо дать время серверу на запуск
        self.create_client_and_start_chat(client_host, client_port, client_name, server_host, server_port)


if __name__ == "__main__":
    main = Main()
    # thread1 = threading.Thread(target=main.start)
    # thread1.start()
    main.start()
    print("hello")
