import json
import socket
from Message import Message
import threading


class Client:

    run = False
    connections: dict = {}

    def __init__(self, host: str = '127.0.0.1', port: int = 2550, name: str = "test"):
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

        thread = threading.Thread(target=self.receive)
        thread.start()

    def connect(self, address):
        self.socket.connect(address)
        message = Message(
            status="join",
            host=self.host,
            port=self.port,
            name=self.name
        )
        self.socket.send(message.to_json().encode("utf-8"))

    def receive(self):
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            if data['status'] == 'connections':
                self.connections = data['connections']
                print(self.connections)

    def send(self):
        pass