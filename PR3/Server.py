import json
import socket
import threading

from Message import Message


class Server:

    socket = None
    connections: dict = {}
    run = False

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.run = True

    def send(self, address: tuple):
        message = Message(
            status="connections",
            connections=self.connections
        )
        self.socket.sendto(message.to_json().encode("utf-8"), address)

    def receive(self):
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            print(data)
            if data['status'] == "join":
                self.send(addr)
                print("Hello,", addr)
            self.connections[str(addr)] = data['name']

    def run_server(self):
        thread = threading.Thread(target=self.receive)
        thread.run()


if __name__ == "__main__":
    server = Server("127.0.0.1", 2550)
    server.run_server()

