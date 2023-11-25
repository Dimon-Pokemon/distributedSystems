import json
import socket
import threading

from Status import Status
from Message import Message
from Main import Main


class Client:

    run = False
    connections: dict = {}

    main: Main = None

    def __init__(self, main: Main, host: str = '127.0.0.1', port: int = 2550, name: str = "test"):
        self.main = main

        self.host = host
        self.port = port
        self.name = name
        self.address = (host, port)
        self.list_connections: list = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Запускаем "прослушивание" указанного адреса:
        self.socket.bind(self.address)

        self.run = True

    def start_receive(self):
        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

    def connect(self, address):
        self.socket.connect(address)
        message = Message(
            status=Status.JOIN.value,
            host=self.host,
            port=self.port,
            name=self.name
        )
        self.socket.send(message.to_json().encode("utf-8"))

    def receive(self):
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            if data['status'] == Status.CONNECTIONS.value:
                self.connections = data['connections']
                print(self.connections)
            # Если в сообщении информация о новом клиенте чата
            elif data['status'] == Status.NEW_CLIENT_INFO.value:
                # Добавляем клиента в список подключений
                self.connections[data['address']] = data['name']
                self.main.update_listBox(data['name'])

    def send(self):
        pass
