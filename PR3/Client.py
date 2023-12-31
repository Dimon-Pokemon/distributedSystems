import json
import socket
import sys
import threading

from Status import Status
from Message import Message
from Main import Main

from Node import Node


# Класс клиента Client наследуется от Node
class Client(Node):

    run = False
    # connections: dict = {} # Список соединений вида name:address
    # socket = None

    main: Main = None

    def __init__(self, main: Main, host: str = '127.0.0.1', port: int = 2550, name: str = "test"):
        self.main = main

        self.host = host
        self.port = port
        self.name = name
        self.address = (host, port)
        self.list_connections: list = None # Список соединений

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Запускаем "прослушивание" указанного адреса:
        self.socket.bind(self.address)

        self.run = True

    def start_receive(self):
        """Метод запускает обработку полученных сообщений в отдельном потоке"""
        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

    def connect(self, address):
        """Метод для подклчения к узлу чата."""
        message = Message(
            status=Status.JOIN.value,
            host=self.host,
            port=self.port,
            name=self.name
        )
        if self.address == address:
            print("Подключение к самому себе невозможно")
        else:
            self.socket.sendto(message.to_json().encode("utf-8"), address)

    def exit(self, address_chat_node):
        """Метод для выхода из чата. Уведомляет всех клиентов чата о том, что данный клиент выходит из чата."""
        message = Message(
            status=Status.EXIT.value,
            name=self.name
        )
        byte_json_message = message.to_json().encode('utf-8')
        self.socket.sendto(byte_json_message, address_chat_node)
        # Перебираем все соединения из списка соединений
        for address in self.connections.values():
            host, port = address.split(":")
            self.socket.sendto(byte_json_message, (host, int(port)))
        self.socket.close()
        sys.exit(0)

    def receive(self):
        """Метод обработки входящих сообщений"""
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            if data['status'] == Status.MESSAGE.value: # Если это обычное сообщение
                self.main.print_new_message_from_client(data['text'], data['from_name'])
            elif data['status'] == Status.CONNECTIONS.value: # Если это сообщение со списком клиентов в чате
                self.connections = data['connections']
                print(self.connections)
                for client_name in self.connections.keys():
                    self.main.chats_history[client_name] = []
            elif data['status'] == Status.NEW_CLIENT_INFO.value: # Если сообщение с информацией о новом клиенте
                # Добавляем клиента в список подключений
                self.connections[data['name']] = data['address']
                self.main.chats_history[data['name']] = []
                self.main.update_listBox(data['name'])
            elif data['status'] == Status.EXIT.value: # Если сообщение о выходе одного из клиентов из чата
                # Удаление вышедшего клиента из списка участников чата
                self.connections.pop(data['name'])
                self.main.delete_client(data['name'])
            elif data['status'] == Status.JOIN.value: # Если сообщение о подключении нового пользователя к чату
                '''connections не содержит адрес самого клиента.
                А так как он отсылает список клиентов(connections) чата новому узлу,
                то требуется добавить в список еще "себя" 
                '''
                print("К чату подключаются через клиента")
                connections: dict = self.connections.copy() # Создаем новую локальную переменную-копию connections
                connections[self.name] = self.convert_tuple_address_to_string(self.address) # Добавляем себя в список
                print("Connections: ", connections)
                self.send_connections_to_new_client(addr, connections) # Отправляем новому клиенту список участников чата, включая себя

                print("Hello,", addr)
                # Рассылаем участникам чата информацию о новом клиенте
                self.send_info_about_new_client(addr, data['name'])
                # Обновляем свой список соединений, добавив нового клиента
                self.connections[data['name']] = self.convert_tuple_address_to_string(addr)
                # Добавялем пустую историю сообщений с новым клиентом
                self.main.chats_history[data['name']] = []
                # Обновляем UI
                self.main.update_listBox(data['name'])

    def send(self, to, message: Message):
        """Метод отправки сообщения удаленному клиенту"""
        print("Список участников чата:", self.connections)
        byte_json_message = message.to_json().encode('utf-8')
        host, port = self.connections[to].split(":")
        self.socket.sendto(byte_json_message, (host, int(port)))
        print("Сообщение отправлено!")
