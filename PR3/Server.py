import argparse
import json
import socket
import threading

from Status import Status
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

    def convert_tuple_address_to_string(self, addr: tuple) -> str:
        """
        Преобразует адрес в виде кортежа в адрес в виде строки вида "IP:PORT",

        Подробности:
            Для отправки сообщений socket.sendto требуется указать адрес в виде кортежа
            ('127.0.0.1', 2551), где порт представлен в виде числа, а хост в виде строки.
            А список подключений представлен в виде словаря dict и имеет вид
            connections = {"127.0.0.1:2551": "name", "127.0.0.1:2552": "name2"} -
            это нужно для нормального преобразования в объект JSON, потому что если ключом будет КОРТЕЖ, то
            преобразования будет некорректым.

        """
        return ":".join((addr[0], str(addr[1])))

    def send_connections_to_new_client(self, address: tuple):
        message = Message(
            status=Status.CONNECTIONS.value,
            connections=self.connections
        )
        self.socket.sendto(message.to_json().encode("utf-8"), address)

    def send_info_about_new_client(self, address_new_client: tuple, name_new_client: str):
        message = Message(
            status=Status.NEW_CLIENT_INFO.value,
            address=self.convert_tuple_address_to_string(address_new_client),
            name=name_new_client
        )
        byte_json_message = message.to_json().encode("utf-8")
        for address_client in self.connections.values():
            # В словаре соединений адреса хронятся в виде строк '127.0.0.1:2551'
            # а для отправки на сокет данных нужен адрес в виде кортежа ('127.0.0.1', 2551)
            tuple_address_client = address_client.split(":") # Получаем список вида ['127.0.0.1', '2551']
            tuple_address_client = (tuple_address_client[0], int(tuple_address_client[1])) # Получаем кортеж вида ('127.0.0.1', 2551)
            self.socket.sendto(byte_json_message, tuple_address_client)
    #
    # def send_error_duplicate_name(self, address, name):
    #     message = Message(
    #         status=Status.ERROR_DUPLICATE_NAME.value,
    #         name=name
    #     )
    #     byte_json_message = message.to_json().encode("utf-8")
    #     self.socket.sendto(byte_json_message, address)

    def receive(self):
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            print(data)
            if data['status'] == Status.JOIN.value:
                if data["name"] in self.connections:
                    pass
                    # self.send_error_duplicate_name(addr, data['name'])
                else:
                    self.send_connections_to_new_client(addr)
                    print("Hello,", addr)
                    self.send_info_about_new_client(addr, data['name'])
                    self.connections[data['name']] = self.convert_tuple_address_to_string(addr)

    def run_server(self):
        thread = threading.Thread(target=self.receive)
        thread.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", default=2550, type=int)
    args = parser.parse_args()

    server = Server(args.host, args.port)
    server.run_server()

