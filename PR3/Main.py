import os
import sys
import threading
import time

from UserInterface import UserInterface
from Message import Message
from Status import Status
# from tkinter import *


class Main:
    client: 'Client' = None
    userInterface: UserInterface = None
    chats_history: dict = {} # История переписки клиента с другими участниками чата
    selected_chat: str = None # Имя клиента чата, который выбран для переписки

    '''address_chat_node - это участник чата или сигнальный сервер. При запуске приложения мы указываем ip и port этого
     участника чата/сигнального сервера. К нему новый клиент обращается чтобы получить сведения о других
      участниках(клиентах) чата.'''
    address_chat_node = None # Может быть сервером или клиентом чата

    def __init__(self):
        self.userInterface = UserInterface(self)

    def start(self):
        """Метод запуска стартового экрана GUI"""
        self.userInterface.start_window_create_or_connect_to_chat()

    def update_listBox(self, name):
        """Метод для обновления списка подклчений на GUI"""
        self.userInterface.listbox_connections.insert(0, name)

    def set_selected_chat(self, name):
        """Установка выбранного на GUI клиента для обмена сообщениями"""
        self.selected_chat = name

    def delete_client(self, name_client_which_exit):
        """Метод для удаления отключивышего клиента с GUI и истории"""
        # Удаление истории переписки с вышедшим клиентом
        self.chats_history.pop(name_client_which_exit)
        # Удаление вышедшего клиента из GUI
        self.userInterface.delete_name_from_listbox(name_client_which_exit)

    def exit(self):
        """Метод для выхода из приложения"""
        self.client.exit(self.address_chat_node) # Вызываем метод уведомления всех участникам чата о выходе клиента из чата
        sys.exit(0) # Завершение работы

    def get_chat_history(self, name: str):
        """Метод для получения истории сообщений с конкретным клиентом чата"""
        return self.chats_history[name]

    def send(self, to_name, text_message):
        """Метод для подготовки сообщения к отправке"""
        message = Message(
            status=Status.MESSAGE.value,
            position='right',
            to_name=to_name,
            from_name=self.client.name,
            text=text_message
        )
        self.chats_history[to_name].append(message) # Обновляем историю сообщений
        self.userInterface.print_message(message) # Добавляем новое сообщения на GUI
        self.client.send(to_name, message) # Передаем сообщение на отправку в объект Client

    def print_new_message_from_client(self, text_message, name):
        """
        Метод создает Message ндля отображения присланного сообщения, сохраняет его в историю и передает в GUI для
        вывода в окне чата.
        """
        message = Message(
            position='left',
            text=text_message
        )
        self.chats_history[name].append(message)
        if name == self.selected_chat:
            self.userInterface.print_message(message)

    def create_client_and_connect_to_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        from Client import Client
        host = client_host
        port = client_port
        name = client_name

        # Создание клиента
        self.client = Client(self, host, port, name)

        # Запускаем на клиенте обработку входящих сообщений
        self.client.start_receive()

        # Устанавливаем адрес узла чата(сервер или другой клиент чата)
        self.address_chat_node = (server_host, server_port)

        # Запускаем метод для подсоединения к узлу чата
        self.client.connect(self.address_chat_node)

    def create_client_and_start_chat(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        # Создание клиента и подключение к чату
        self.create_client_and_connect_to_chat(client_host, client_port, client_name, server_host, server_port)
        # Уничтожение окна ввода данных для создания клиента (Client) и данных для подключения к чату/его создания
        self.userInterface.connectToChatWindow.destroy()
        # Запуск интерфейса чата
        self.userInterface.start_main_window(client_name, client_host, client_port)

    def create_server(self, client_host: str, client_port: int, client_name: str, server_host: str, server_port: int):
        """
        Метод для создания сервера (срабатывает при нажатии на кнопку 'Создать чат' в окне подсоединения к чату)
        и подключения к нему.
        """
        # Запуск сервера командрй консоли
        thread = threading.Thread(target=os.system, daemon=True, args=[f"python3 Server.py --host {server_host} --port {server_port}"])
        thread.start()
        time.sleep(10) # Надо дать время серверу на запуск
        # Создание клиента и подключение к чату
        self.create_client_and_start_chat(client_host, client_port, client_name, server_host, server_port)

# Точка входа в программу
if __name__ == "__main__":
    main = Main()
    # thread1 = threading.Thread(target=main.start)
    # thread1.start()
    main.start()
    print("hello")
